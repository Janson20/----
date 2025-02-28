;汉化：MonKeyDu 
;由 Inno Setup 脚本向导 生成的脚本,有关创建 INNO SETUP 脚本文件的详细信息，请参阅文档！!

#define MyAppName "智能单词本"
#define MyAppVersion "2.0"
#define MyAppPublisher "刘嘉晟"
#define MyAppExeName "智能单词本.exe"

[Setup]
;注意：AppId 的值唯一标识此应用程序。请勿在安装程序中对其他应用程序使用相同的 AppId 值。
;（若要生成新的 GUID，请单击“工具”|”在 IDE 中生成 GUID）。
AppId={{A0A8D98C-1256-4194-9481-0D22CAAD9EAD}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
; "ArchitecturesAllowed=x64compatible" 指定安装程序无法运行
;在 Arm 上的 x64 和 Windows 11 以外的任何东西上.
ArchitecturesAllowed=x64compatible
; "ArchitecturesInstallIn64BitMode=x64compatible" 请求
;在 x64 或 Arm 上的 Windows 11 上以“ 64 位模式”进行安装，,
;这意味着它应该使用本机 64 位 Program Files 目录和
;注册表的 64 位视图.
ArchitecturesInstallIn64BitMode=x64compatible
DisableProgramGroupPage=yes
LicenseFile=G:\Python\比赛作品\编译\隐私协议.txt
; 取消下列注释行，在非管理员安装模式下运行(仅为当前用户安装.)
;PrivilegesRequired=lowest
OutputDir=G:\Dist
OutputBaseFilename=Setup
SetupIconFile=G:\Python\比赛作品\ico.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "chs"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "G:\Python\比赛作品\编译\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "G:\Python\比赛作品\编译\wordbook.json"; DestDir: "{app}"; Flags: ignoreversion
; 注意:  在任何共享系统文件上不要使用 "Flags: ignoreversion"

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

