
/**
 *
 * @author Anurag
 */
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.*;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.logging.Level;
import java.util.logging.Logger;

public class Server extends Thread {

    private static final int PORT = 7520;
    private ServerSocket listener = null;
    BufferedReader input;
    PrintWriter output;
    String name;

    Server() throws IOException {
        listener = new ServerSocket(PORT);
    }

    public void run() {
        Utils.logServer("Server Listening on port : " + listener.getLocalPort());
        try {
            Socket cliListener = listener.accept();
            Utils.logServer("Connected to " + cliListener.getRemoteSocketAddress());
            input = new BufferedReader(new InputStreamReader(cliListener.getInputStream()));
            output = new PrintWriter(cliListener.getOutputStream(), true);

            receiveExpected("Hello");
            send("Hello");
            receiveExpected("ACK");

            send("DATA1");
            receiveExpected("ACK");

            receiveExpected("DATA2");
            send("ACK");

            receiveExpected("Disconnecting");
            send("ACK");

            Utils.logServer("[ Disconnected ]");

        } catch (Exception e) {
            Utils.logServer(e.getMessage());
        }
    }

    public static void main(String[] args) throws IOException {
        Thread t = new Server();
        t.start();
    }

    public void send(String msg) {
        try {
            output.println(msg);
            Utils.logServer("[ Sent ] " + msg);
        } catch (Exception ex) {
            Utils.logServer("[ error ] could not send msg");
        }
    }

    public void receiveExpected(String expectedMessage) throws Exception {
        if (! expectedMessage.equals(receive())) {
            throw new Exception("[ Protocol error ]");
        }
    }

    public String receive() throws Exception {
        String s = input.readLine();
        Utils.logServer("[ Received ] " + s);
        return s;
    }
}
