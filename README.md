# Image Transmission via UDP Sockets Using Sliding Window Protocol
This project involves building a reliable image transmission system using the UDP (User Datagram Protocol). The system is designed to handle the sending of images between a sender and receiver over a network, using a Sliding Window Protocol to ensure that the packets (data chunks) are transmitted efficiently and reliably, despite the inherent unreliability of UDP. The project includes two main components: the Sender and the Receiver, which communicate over a socket connection.

## **2-Project Overview:** 
This project involves building a reliable image transmission system using the UDP (User Datagram Protocol). The system is designed to handle the sending of images between a sender and receiver over a network, using a Sliding Window Protocol to ensure that the packets (data chunks) are transmitted efficiently and reliably, despite the inherent unreliability of UDP. The project includes two main components: the Sender and the Receiver, which communicate over a socket connection.

## **3-Techniques Used:**
### **3.1 Sliding Window Protocol**
The project implements a Go-Back-N version of the sliding window protocol to ensure reliable data transmission. This technique involves:

- **Sending multiple packets at once (window size), where each packet is identified by a unique ID.**
- **Waiting for acknowledgments (ACKs) from the receiver before sliding the window and sending new packets.**
- **Retransmitting lost or timed-out packets based on the acknowledgments received.**


 ### **3.2 Chunking and Bit Manipulation**
The images are converted into binary data streams, and these streams are then divided into smaller chunks (packets). Each packet contains:

- **Packet ID: Identifies the specific packet in the sequence.**
- **File ID: Identifies the image being sent.**
- **Trailer: A marker that indicates whether the packet is the last one.**


 ### **3.3 Timeout and Retransmission**
To account for network unreliability, a timeout mechanism is implemented. If a packet is sent and an acknowledgment is not received within a specified time, the sender retransmits the packet. This ensures that the receiver eventually gets all the packets, even if some are lost during transmission.


## **4 Libraries and Tools Used:**

**Python Socket Library**
The Python socket library is used to create the UDP communication channels. The sender opens a socket and transmits data, while the receiver listens for incoming packets and sends acknowledgments.

- **socket.sendto(): Sends data to the receiver.**
- **socket.recvfrom(): Receives data from the sender.**


**OpenCV (cv2)**
The cv2 library is part of OpenCV, an open-source computer vision library. It is used to handle image processing tasks such as:

- **Reading images from files (cv2.imread()).**
- **Encoding images to bytes (cv2.imencode()).**
- **Decoding received bytes back into an image (cv2.imdecode()).**
- **Writing the reconstructed image to disk (cv2.imwrite()).**

** NumPy**
NumPy is a fundamental library for array processing in Python. In this project, it is used to handle byte manipulation and the conversion of binary data back into images. Specifically, NumPy arrays are used to manage the binary streams and reconstruct images.

## **5 Implementation Details: **
**Sender**
The sender is responsible for:

- **Loading images from disk using cv2.imread().**
- **Converting images into a binary stream by encoding the image into JPEG format (cv2.imencode()) and converting the byte data into a binary string.**
- **Chunking the binary data into packets, each with a packet ID, file ID, and trailer. The trailer is used to indicate whether the packet is the last one (0xFFFF for the final packet, 0x0000 for all others).**
- **Transmitting the packets over a UDP socket using the sliding window protocol, ensuring that any lost packets are retransmitted based on acknowledgment timeouts.**


**Receiver**
The receiver is responsible for:

- **Listening for incoming packets over the UDP socket.**
- **Processing each packet to extract its data (packet ID, file ID, and image data) and checking the trailer to determine if it's the last packet.**
- **Reassembling the image once all packets are received, using cv2.imdecode() to convert the binary stream back into an image.**
- **Sending acknowledgments for correctly received packets and requesting retransmission for lost ones.**

## **6 Challenges and Solutions**
**6.1 Unreliable UDP Transmission**:
UDP does not guarantee that packets will be delivered in the correct order, or even at all. The use of a sliding window protocol, along with acknowledgment and retransmission, ensures that the transmission is made reliable.

**6.2 Packet Loss and Timeout Management**:
Managing packet loss was a significant challenge. This was solved by implementing a timeout mechanism, where the sender waits for an acknowledgment for each packet and resends packets that are not acknowledged within the specified timeout period.

**6.3 Handling Large Images**:
The binary data generated from large images can result in a large number of packets. By adjusting the window size and timeout values, the project optimizes the transmission speed and reduces the number of retransmissions.


## **7 Performance Metrics**
Performance metrics are measured and displayed after each image transmission. These include:

- **Total Transmission Time: The time taken to send an entire image.**
- **Total Number of Packets: The number of packets required to send the image.**
- **Number of Retransmissions: How many packets had to be resent due to packet loss or timeout.**
- **Transmission Rate: The number of packets sent per second, which helps evaluate the efficiency of the transmission process.**





This project successfully simulates a reliable image transmission system over an unreliable network using UDP and a custom sliding window protocol. The system can handle packet loss, timeouts, and retransmissions, ensuring that large images are transmitted without data loss. By leveraging Python libraries like socket, OpenCV, and NumPy, the project efficiently processes image data and simulates a real-world network communication scenario.






## **Future Enhancements**
Future improvements could include:

Adding support for larger data files such as videos.
Implementing congestion control to optimize transmission speed over congested networks.
Using more advanced error detection techniques like CRC (Cyclic Redundancy Check) to verify data integrity beyond basic acknowledgment.
