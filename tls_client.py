import sys
import ssl
import socket
import argparse
import OpenSSL


class Client:
    def __init__(self, args):

        parser = argparse.ArgumentParser()
        parser.add_argument("--tlsv1.0", action="store_true")
        parser.add_argument("--tlsv1.1", action="store_true")
        parser.add_argument("--tlsv1.2", action="store_true")
        parser.add_argument("--sslv3", action="store_true")
        parser.add_argument("--ciphers", dest="ciphers", default="")
        parser.add_argument("--cacert", dest="certificate")
        parser.add_argument("trail", nargs=argparse.REMAINDER)
        inputs = parser.parse_args()

        version = ""
        d = vars(inputs)
        if d['tlsv1.0']:
            version = ssl.PROTOCOL_TLSv1
        elif d['tlsv1.1']:
            version = ssl.PROTOCOL_TLSv1_1
        elif d['tlsv1.2']:
            version = ssl.PROTOCOL_TLSv1_2
        else:
            version = ssl.PROTOCOL_SSLv23
        accepted_ciphers = inputs.ciphers
        trail = inputs.trail
       
        # 1. Instantiating an SSL/TLS context
        context = ssl.create_default_context()
        context.verify_mode = (ssl.CERT_REQUIRED)

        # 4. Instantiating a TCP socket
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 5. Wrapping the TCP socket with the SSL/TLS context
        if (inputs.certificate==None):
            context.load_default_certs()
        wrapped = ssl.wrap_socket(self.s, ca_certs=inputs.certificate, ssl_version=version, ciphers=accepted_ciphers)
        #socket.conect(sslHost, sslPort, ssl)

        wrapped.connect((trail[0], int(trail[1])))
       


        #get and print certificate
        print 'getting cert'
        peerCert = wrapped.getpeercert(True)
        readable = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_ASN1, peerCert)
        #print(peerCert)
        #OpenSSL.crypto.dump_certificate(type, cert)
        plainText = readable.get_subject().get_components()
        print(plainText)
         #z = ssl.get_server_certificate( (trail[0], int(trail[1])), ssl_version=version )

        # 6. Initiate a connection (to a SSL/TLS server at port 443) & perform a HTTP GET
        wrapped.send("GET /"+ trail[2] + " HTTP/1.0\n\n")
        go = True
        while (go):
            response = self.s.recv(4096)
            if response == "":
                go = False
                print(response)
        # 7. Closing the socket
        self.s.close()
        wrapped.close()

def main(args):
	start = Client(args)

if __name__ == "__main__":
	main(sys.argv)

    
    

# 2. Setting TLS/SSL client options

# 3. Setting the default TLS root certificate paths (e.g., with load_default_certs())
    #context.load_default_certs()


#EX COMMDANLINE INPUT:
#tls_client.py --tlsv1.1 --ciphers DHE-DSS- AES256-SHA:DH-RSA-AES256-SHA 10.0.0.1 443 file.txt