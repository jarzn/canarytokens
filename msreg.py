from cStringIO import StringIO

REG_TEMPLATE = """Windows Registry Editor Version 5.00
; Sensitive command token generated by Thinkst Canary
; Run with admin privs on Windows machine as: reg import FILENAME

; command that will be watched for
[HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\{PROCESS}]
"GlobalFlag"=dword:00000200

; magic unique canarytoken that will be fired when this command is executed
[HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\SilentProcessExit\{PROCESS}]
"ReportingMode"=dword:00000001
"MonitorProcess"="cmd.exe /c start /min powershell.exe -windowstyle hidden -command \\\"&{{Resolve-DnsName -Name \\\\\\\"$env:computername.UN.$env:username.CMD.{TOKEN_DNS}\\\\\\\"}}\\\""
"""

def make_canary_msreg(url=None, process_name='klist.exe'):
    if process_name.find('.exe') == -1:
        process_name += '.exe'
    output_buf = StringIO(REG_TEMPLATE.format(TOKEN_DNS=url, PROCESS=process_name))
    return output_buf.getvalue()

