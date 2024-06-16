# EasyRemoveBG

## Description

The EasyRemoveBG is a simple application that allows users to remove the background from photos using a right-click context menu option in Windows Explorer.

## Features

- Right-click integration in Windows Explorer for easy access.
- Background removal functionality using advanced algorithms.
- Supports various image formats (e.g., PNG, JPEG, WEBP).

## Technologies Used

- **Remove Background:**
  - Suitable for normal photos.
  - Uses [Rembg](https://pypi.org/project/rembg/) for background removal.

- **Remove Logo:**
  - Recommended for logos and graphics.
  - Uses [OpenCV](https://opencv.org/) for logo removal, which provides effective handling of shapes and contours.

## Requirements

- Windows operating system
- Python 3.12 or later installed
- Required Python packages (install using `pip install -r requirements.txt`)

## Setup Instructions

1. **Download or Clone the Repository:**
   - Download or clone the repository to your local machine.

2. **Run `first.bat` Script:**
   - Double-click on `first.bat` located in the root of the repository to initialize the setup process. This script will prepare the environment and install necessary dependencies.

3. **Import `second.reg` File:**
   - After `first.bat` completes, you can import `second.reg` into the Windows registry to add the right-click context menu options.

By following these instructions, users should be able to easily set up and start using your EasyRemoveBG on their Windows systems.

## Usage

- Navigate to a folder containing images.
- Right-click on an image file (e.g., `example.jpg`).
- Select "Remove Background" or "Remove Logo" from the context menu to process the image.

## Contributing to EasyRemoveBG

### Logo for Right-Click Menu

#### Logo Requirement:
- We need a logo to represent the EasyRemoveBG in the right-click context menu.
- The logo should be visually appealing and clear even at smaller sizes.
- Preferably, provide the logo in vector format (SVG) for scalability.

### Integration of Submenus

#### Integrating Remove Logo and Remove Background:

- If possible, contributors are encouraged to explore integrating both "Remove Logo" and "Remove Background" options into a single right-click menu.
- Submenus can enhance user experience by organizing functionalities logically.
- Consider usability and design principles when proposing or implementing this feature.



