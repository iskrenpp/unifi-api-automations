# 📡 UniFi API Scripts
>
> ⚠️ **NOTE:** UniFi API for updates like PUT is blocking clients with a 403 error if attempted remotely. The API scripts work only when POST/PUT are executed against UniFi localhost on port 443.
>
 ## 🔀 Port Forwarding Rule Enable/Disable Control

 **🎯 Use Case:** Temporary access through the firewall to a specific host, such as Nginx-proxy-manager for Let's Encrypt DNS challenge passing. We can use a script like `unifi-control-port-forwarding-rules.py`. Being a script, we can automate the rule enable/disable at desired intervals. Since the UniFi host does not have crontab, we should execute the script locally on the UniFi host but with a remote execution trigger. The UniFi controller must have SSH enabled and set up.

 **📋 Example command:** This command can fully automate the control of port forwarding rules from any remote machine that has crontab while the API Python script is still executed locally on the UniFi controller:

 ```
 sshpass -p '<unifi-root-password>' ssh root@<unifi-ip-address> "python ~/unifi-api.py --rule_name '<Rule name as described in the WEB UI>' --new_enable_value <True|False>"
 ```

 **🔒 Security:** For security reasons, we can set up the password to be read from the SSHPASS environment variable with `sshpass -e ...`. Then, the cron will be something like this:

 ```
 <cron expression> source /path/to/pass.txt && ( sshpass -e ssh root@<unifi-ip-address> "python ~/unifi-api.py --rule_name '<Rule name as described in the WEB UI>' --new_enable_value <True|False>" )
 ```

 **🔑 SSH Key:** Keep in mind that if you try to run the cron command from a remote host that has never completed a successful SSH connection to the UniFi controller, you must either run `ssh root@<unifi-controller-ip>` manually and accept the SSH key of the remote host with 'Yes', or pass the SSH key skipping option `-o StrictHostKeyChecking=no` to SSH like this:

 ```
 <cron expression> source /path/to/pass.txt && ( sshpass -e ssh -o StrictHostKeyChecking=no root@<unifi-ip-address> "python ~/unifi-api.py --rule_name '<Rule name as described in the WEB UI>' --new_enable_value <True|False>" )
 ```
