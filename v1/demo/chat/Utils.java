import java.text.SimpleDateFormat;
import java.util.Date;

public class Utils {

    public static void logClient(String message) {
        log("Client", message);
    }

    public static void logServer(String message) {
        log("Server", message);
    }

    public static void log(String agent, String message) {
        String timeStamp = new SimpleDateFormat("yyyy.MM.dd-HH.mm.ss.S").format(new Date());
        System.out.printf("%s %s %s\n", timeStamp, agent, message);
    }
}
