# python-avro-rpc-pcap
Simple python client/server to generate and capture AVRO pcap records

Configure virtual environment


Start the server
workon python-avro-rpc-pcap
cd src
python avro_rpc_server

Start the packet capture
sudo tcpdump -vvv -i lo0 -s 0 -B 524288 -w avro.pcap port 5000

Run the server
python client

