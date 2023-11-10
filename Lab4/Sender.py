import argparse
import RDT
import time

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Quotation sender talking to a receiver."
    )
    parser.add_argument("receiver", help="receiver.")
    parser.add_argument("port", help="Port.", type=int)
    args = parser.parse_args()

    msg_L = [
        "sending message - 1",
        "sending message - 2",
        "sending message - 3",
        "sending message - 4",
        "sending message - 5",
        "sending message - 6",
        "sending message - 7",
        "sending message - 8",
        "sending message - 9",
        "sending message - 10",
    ]

    timeout = 2  # send the next message if no response
    time_of_last_data = time.time()

    rdt = RDT.RDT("sender", args.receiver, args.port)
    for msg_S in msg_L:
        print("Sent Message: " + msg_S)
        rdt.rdt_1_0_send(msg_S)

        # try to receive message before timeout
        msg_S = None
        while msg_S == None:
            msg_S = rdt.rdt_1_0_receive()
            if msg_S is None:
                if time_of_last_data + timeout < time.time():
                    break
                else:
                    continue
        time_of_last_data = time.time()

        # print the result
        if msg_S:
            print("Received Message: " + msg_S + "\n")

    rdt.disconnect()
