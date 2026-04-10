#define MyAppName "EasyRemoveBG"
#define MyAppVersion "1.1.0"
#define MyAppPublisher "EasyRemoveBG"
#define MyAppExeName "EasyRemoveBG.exe"
#define MyAppDistDir "..\dist\EasyRemoveBG"

[Setup]
AppId={{A8D0CA6E-B02F-4720-86AA-EA8B8895A5E7}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={localappdata}\Programs\{#MyAppName}
DefaultGroupName={#MyAppName}
UninstallDisplayIcon={app}\{#MyAppExeName}
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
OutputDir=Output
OutputBaseFilename=EasyRemoveBG-Setup

[Files]
Source: "{#MyAppDistDir}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\Uninstall {#MyAppName}"; Filename: "{uninstallexe}"

[Registry]
Root: HKCU; Subkey: "Software\Classes\SystemFileAssociations\image\shell\EasyRemoveBG.RemoveBackground"; ValueType: string; ValueName: ""; ValueData: "Remove Background"; Flags: uninsdeletekey
Root: HKCU; Subkey: "Software\Classes\SystemFileAssociations\image\shell\EasyRemoveBG.RemoveBackground"; ValueType: string; ValueName: "Icon"; ValueData: "{app}\{#MyAppExeName}"
Root: HKCU; Subkey: "Software\Classes\SystemFileAssociations\image\shell\EasyRemoveBG.RemoveBackground\command"; ValueType: string; ValueName: ""; ValueData: """{app}\{#MyAppExeName}"" remove-bg ""%1"""; Flags: uninsdeletekey
Root: HKCU; Subkey: "Software\Classes\SystemFileAssociations\image\shell\EasyRemoveBG.RemoveLogoBackground"; ValueType: string; ValueName: ""; ValueData: "Remove Logo Background"; Flags: uninsdeletekey
Root: HKCU; Subkey: "Software\Classes\SystemFileAssociations\image\shell\EasyRemoveBG.RemoveLogoBackground"; ValueType: string; ValueName: "Icon"; ValueData: "{app}\{#MyAppExeName}"
Root: HKCU; Subkey: "Software\Classes\SystemFileAssociations\image\shell\EasyRemoveBG.RemoveLogoBackground\command"; ValueType: string; ValueName: ""; ValueData: """{app}\{#MyAppExeName}"" remove-logo ""%1"""; Flags: uninsdeletekey
