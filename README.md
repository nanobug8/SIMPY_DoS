# SIMPY_DoS
Simulating a DoS attack - Client SSL Renegotiation - mod_ssl 2.4.37 &amp; openssl 1.1.1

CVE 2019-0190

Requirements:
  SimPy version 2.3.1
  
 This code simulates with SimPy parallel SSLConnection and many Renegotiation for each SSLConnection.
 
 Variables:
  time >> represents the CPU time of full handshake.
  (You can observe, capture, and test your CPU time for packets involve in full handsake process)
  R >> Renegotiations
  N >> SSLConnections in parallel
  
Varying this values, you can see differents results on the simulations.
Note that time of CPU depends on Cypher Algorithm.

You can check https://vincent.bernat.ch/en/blog/2011-ssl-dos-mitigation (https://github.com/vincentbernat/ssl-dos)
to get more detailed info for the simulation.

