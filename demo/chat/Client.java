/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

/**
 *
 * @author Anurag
 */
import java.net.*;
import java.io.*;
import java.util.logging.Level;
import java.util.logging.Logger;

public class Client extends Thread {

    private static String serverName;
    private static int PORT;
    BufferedReader input;
    BufferedReader br;
    PrintWriter output;
    Socket server;
    boolean readContinue;

    public Client() {
        this.serverName = "localhost";
        this.PORT = 7520;
    }

    public void run() {
        try {
            Utils.logClient("Connecting to " + serverName + " on port " + PORT + "...");
            server = new Socket(serverName, PORT);

            Utils.logClient("Connected to " + server.getRemoteSocketAddress());
            input = new BufferedReader(new InputStreamReader(server.getInputStream()));
            output = new PrintWriter(server.getOutputStream(), true);
            br = new BufferedReader(new InputStreamReader(System.in));


            send("Hello");
            receiveExpected("Hello");

            send("ACK");

            receiveExpected("DATA1");
            send("ACK");

            send("DATA2");
            receiveExpected("ACK");

            send("Disconnecting");
            receiveExpected("ACK");

            Utils.logClient("[ Disconnected ]");

        } catch (Exception e) {
            Utils.logClient(e.getMessage());
        }
    }

    public void send(String msg) {
        try {
            output.println(msg);
            Utils.logClient("[ Sent ] " + msg);
        } catch (Exception ex) {
            Utils.logClient("[ error ] could not send msg");
        }
    }

    public void receiveExpected(String expectedMessage) throws Exception {
        if (! expectedMessage.equals(receive())) {
            throw new Exception("[ Protocol error ]");
        }
    }

    public String receive() throws Exception {
        String s = input.readLine();
        Utils.logClient("[ Received ] " + s);
        return s;
    }

    public static void main(String[] args) throws IOException {
        Client client = new Client();
        client.run();
    }
}