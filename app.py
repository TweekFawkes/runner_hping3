#!/usr/bin/env python3
import os
import sys
import subprocess
import time

def ensure_output_dir():
    """Create the outputs directory if it doesn't exist."""
    if not os.path.exists("outputs"):
        os.makedirs("outputs")

def run_traceroute(target, command_args, output_filename):
    """Run an hping3 traceroute command and save the output to a file."""
    full_command = ["hping3", target] + command_args
    print(f"Running: {' '.join(full_command)}")
    
    try:
        # Run the command and capture output
        result = subprocess.run(
            full_command, 
            capture_output=True, 
            text=True, 
            check=False  # Don't raise exception on non-zero exit
        )
        
        # Combine stdout and stderr
        output = f"COMMAND: {' '.join(full_command)}\n\n"
        output += f"STDOUT:\n{result.stdout}\n\n"
        output += f"STDERR:\n{result.stderr}\n\n"
        output += f"EXIT CODE: {result.returncode}\n"
        
        # Write output to file
        with open(os.path.join("outputs", output_filename), 'w') as f:
            f.write(output)
            
        print(f"Output saved to outputs/{output_filename}")
        
    except Exception as e:
        print(f"Error running command: {e}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python app.py <target>")
        sys.exit(1)
        
    target = sys.argv[1]
    ensure_output_dir()
    
    # List of traceroute commands to run
    traceroute_commands = [
        # Verbose ICMP Traceroute
        {
            "args": ["--traceroute", "-1", "-V"],
            "filename": "traceroute_icmp.txt"
        },
        # UDP Traceroute to port 53
        {
            "args": ["--traceroute", "-2", "-p", "53", "-V"],
            "filename": "traceroute_udp_port_53.txt"
        },
        # TCP SYN Traceroute to port 80
        {
            "args": ["--traceroute", "-0", "-S", "-p", "80", "-V"],
            "filename": "traceroute_tcp_syn_port_80.txt"
        },
        # TCP ACK Traceroute to port 80
        {
            "args": ["--traceroute", "-0", "-A", "-p", "80", "-V"],
            "filename": "traceroute_tcp_ack_port_80.txt"
        },
        # Using fragmented packets
        {
            "args": ["--traceroute", "-1", "-f", "-V"],
            "filename": "traceroute_fragmented_packets.txt"
        }
    ]
    
    # Run each traceroute command
    for cmd in traceroute_commands:
        run_traceroute(target, cmd["args"], cmd["filename"])
        # Add a short delay between commands
        time.sleep(1)
    
    print(f"All traceroute commands completed. Results saved in the 'outputs' directory.")

if __name__ == "__main__":
    main()

