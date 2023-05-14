# UniFi APi scripts

> NOTE: UniFI APi for updates like PUT is blocking client with 403 if attempted remotely. I have found that the api scripts work only when POST/PUT are executed against UniFI localhost on port 443


- Port forwarding rule enable/disable control

Use Case: When for example you need temporary access through the firewall to specific host, let's say nginx-proxy-manager for Let's Encrypt DNS challenge passing, then we can use script like ```unifi-control-port-forwarding-rules.py```.
Of course being a script we can automate the rule enable/disable at desired intervals.
Since unifi host does not have crontab then we should execute the scipt locally on the unifi host but with remote execution trigger.
It goes without saying that UniFI controller must have ssh enabled and setup.

Here is an example command that can fully automate the control of port forwarding rules from any remote machine that has crontab for example while the api python script is still executed locally on the UniFi controller
```
sshpass -p '<unifi-root-password>' ssh root@<unifi-ip-address> "python ~/unifi-api.py --rule_name '<Rule name as described in the WEB UI>' --new_enable_value <True|False>"
```
Now, for this we need to have package ```sshpass``` installed and for security reasons we can setup the password to be read from SSHPASS env variable with ```sshpass -e ...```
Then the cron will be something like this
```
<cron expresion > source /path/to/pass.txt && ( sshpass -e ssh root@<unifi-ip-address> "python ~/unifi-api.py --rule_name '<Rule name as described in the WEB UI>' --new_enable_value <True|False>" )
```
where ```/path/to/pass.txt``` must be with contents
```
SSHPASS=<unifi-root-pass>
```
Keep in mind that if you try to run the cron command from remote host that has never complted successful ssh to unifi controller then you must either run the ```ssh root@<unif-controller-ip>``` manually and accept with 'Yes' the ssh key of the remote host OR pass the ssh key skipping option ```-o StrictHostKeyChecking=no``` to ssh like
```
<cron expresion > source /path/to/pass.txt && ( sshpass -e ssh -o StrictHostKeyChecking=no root@<unifi-ip-address> "python ~/unifi-api.py --rule_name '<Rule name as described in the WEB UI>' --new_enable_value <True|False>" )
```
