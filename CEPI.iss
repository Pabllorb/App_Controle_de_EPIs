[Setup]
AppName=CadastroDeEpi
AppVersion=0.1
DefaultDirName={pf}\CadastroDeEpi
DefaultGroupName=CadastroDeEpi
OutputBaseFilename=CadastroDeEpiSetup
Compression=lzma
SolidCompression=yes

[Files]
Source: "C:\Users\Windows\Desktop\ControleDeEpi\build*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\CadastroDeEpi"; Filename: "{app}\main.exe"

[Run]
Filename: "{app}\main.exe"; Description: "{cm:LaunchProgram,CadastroDeEpi}"; Flags: nowait postinstall skipifsilent
