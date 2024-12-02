# Screen Security Manager

A Python application to monitor and manage sensitive windows for screen privacy and security in an organization.

## Features
- Detects visible active windows.
- Allows selection of sensitive windows for monitoring.
- Minimizes sensitive windows automatically when detected.

## Prerequisites
- Python 3.8 or later
- Windows OS

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/ScreenSecurityManager.git
    cd ScreenSecurityManager
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the application:
    ```bash
    python src/screen_security_manager.py
    ```


## Usage

1. Select Sensitive Windows:

2. A list of active windows will be displayed. 
   1. Select the windows you want to monitor as "sensitive."

3. Save and Start Monitoring:
   1. Click the "Save and Start Monitoring" button to begin monitoring the selected windows. The application will automatically minimize the windows you selected if they become active.

4. Stop Monitoring:
   1. You can stop monitoring at any time by clicking the "Stop Monitoring" button.
   
5. Monitoring Status:
   1. The status label will show whether monitoring is active or stopped.
## Folder Structure
```plaintext
ScreenSecurityManager/
├── src/                            # Source code
├── tests/                          # Test cases
├── config/                         # Configuration files
├── .gitignore                      # Ignored files
├── LICENSE                         # License file
├── README.md                       # Project description
└── requirements.txt                # Python dependencies
