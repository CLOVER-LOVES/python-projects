"""
Install Voice Assistant as a Windows Service
------------------------------------------
This script installs the voice assistant as a Windows service that starts automatically.
"""

import os
import sys
import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import subprocess
import argparse

class VoiceAssistantService(win32serviceutil.ServiceFramework):
    """
    Windows service for the voice assistant
    """
    _svc_name_ = "VoiceAssistant"
    _svc_display_name_ = "Hey Clover Voice Assistant"
    _svc_description_ = "Runs the Hey Clover voice assistant in the background"
    
    def __init__(self, args):
        """Initialize the service"""
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)
        self.is_running = False
        self.process = None
    
    def SvcStop(self):
        """Stop the service"""
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.is_running = False
        
        # Terminate the process if it's running
        if self.process:
            try:
                self.process.terminate()
            except:
                pass
    
    def SvcDoRun(self):
        """Run the service"""
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_, '')
        )
        self.is_running = True
        self.main()
    
    def main(self):
        """Main service function"""
        # Get the path to the background_assistant.py script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        script_path = os.path.join(script_dir, "background_assistant.py")
        
        # Start the background assistant
        try:
            self.process = subprocess.Popen(
                [sys.executable, script_path, "--start", "--no-tray"],
                cwd=script_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            
            # Wait for the service to stop
            while self.is_running:
                # Check if the process is still running
                if self.process.poll() is not None:
                    # Process has terminated, restart it
                    self.process = subprocess.Popen(
                        [sys.executable, script_path, "--start", "--no-tray"],
                        cwd=script_dir,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        creationflags=subprocess.CREATE_NO_WINDOW
                    )
                
                # Wait for the stop event
                rc = win32event.WaitForSingleObject(self.hWaitStop, 5000)
                if rc == win32event.WAIT_OBJECT_0:
                    # Stop event received
                    break
        except Exception as e:
            servicemanager.LogErrorMsg(f"Error in service: {e}")
        finally:
            # Terminate the process if it's still running
            if self.process and self.process.poll() is None:
                try:
                    self.process.terminate()
                except:
                    pass

def install_service():
    """Install the service"""
    try:
        # Check if running as administrator
        if not is_admin():
            print("This script must be run as administrator to install the service.")
            print("Please right-click on the script and select 'Run as administrator'.")
            return False
        
        # Install the service
        win32serviceutil.HandleCommandLine(VoiceAssistantService)
        return True
    except Exception as e:
        print(f"Error installing service: {e}")
        return False

def is_admin():
    """Check if the script is running with administrator privileges"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def create_startup_shortcut():
    """Create a shortcut in the Windows startup folder"""
    try:
        # Get the path to the background_assistant.py script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        script_path = os.path.join(script_dir, "background_assistant.py")
        
        # Get the path to the startup folder
        startup_folder = os.path.join(
            os.environ["APPDATA"],
            "Microsoft\\Windows\\Start Menu\\Programs\\Startup"
        )
        
        # Create a batch file to run the script
        batch_path = os.path.join(script_dir, "run_assistant.bat")
        with open(batch_path, "w") as f:
            f.write(f'@echo off\n')
            f.write(f'start "" /min "{sys.executable}" "{script_path}" --start\n')
        
        # Create a shortcut to the batch file
        shortcut_path = os.path.join(startup_folder, "Hey Clover Voice Assistant.lnk")
        
        # Use Windows Script Host to create the shortcut
        with open("create_shortcut.vbs", "w") as f:
            f.write(f'Set oWS = WScript.CreateObject("WScript.Shell")\n')
            f.write(f'sLinkFile = "{shortcut_path}"\n')
            f.write(f'Set oLink = oWS.CreateShortcut(sLinkFile)\n')
            f.write(f'oLink.TargetPath = "{batch_path}"\n')
            f.write(f'oLink.WorkingDirectory = "{script_dir}"\n')
            f.write(f'oLink.Description = "Hey Clover Voice Assistant"\n')
            f.write(f'oLink.Save\n')
        
        # Run the VBScript
        os.system("cscript //nologo create_shortcut.vbs")
        
        # Delete the VBScript
        os.remove("create_shortcut.vbs")
        
        print(f"Startup shortcut created: {shortcut_path}")
        return True
    except Exception as e:
        print(f"Error creating startup shortcut: {e}")
        return False

def main():
    """Main function"""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Install the voice assistant as a Windows service")
    parser.add_argument("--service", action="store_true", help="Install as a Windows service (requires admin)")
    parser.add_argument("--startup", action="store_true", help="Create a startup shortcut")
    args = parser.parse_args()
    
    # Check if no arguments were provided
    if not args.service and not args.startup:
        parser.print_help()
        return
    
    # Install as a service if requested
    if args.service:
        if install_service():
            print("Service installed successfully.")
        else:
            print("Failed to install service.")
    
    # Create a startup shortcut if requested
    if args.startup:
        if create_startup_shortcut():
            print("Startup shortcut created successfully.")
        else:
            print("Failed to create startup shortcut.")

if __name__ == "__main__":
    main()
