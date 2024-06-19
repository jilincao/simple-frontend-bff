# Install
run `pnpm install`

# env file

# Start Server
npx next dev -H 0.0.0.0 -p 9070

conda activate /mnt/sgnfsdata/tolo-03-97/jilincao/env/py12

# When a port is used, or you need to stop the server
It seems that port 3000 is already in use by another process.

If you use Linux as OS:

For a list of listening ports
`ss -ntlp`
or
`netstat -ntlp`
To check specifically for port 3000
netstat -ntlp | grep ':3000'
Next, kill the process using the port (check what it is first).

kill <PID>
kill -9 <PID> # if kill does not work
If you're using Windows or macOS, there's an equivalent way to list listening ports and kill the process using the desired port.

