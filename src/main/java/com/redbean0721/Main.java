package com.redbean0721;

import io.github.cdimascio.dotenv.Dotenv;
import net.dv8tion.jda.api.JDA;
import net.dv8tion.jda.api.JDABuilder;
import net.dv8tion.jda.api.OnlineStatus;
import net.dv8tion.jda.api.entities.Activity;
import net.dv8tion.jda.api.exceptions.InvalidTokenException;
import net.dv8tion.jda.api.requests.GatewayIntent;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.yaml.snakeyaml.Yaml;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.util.Map;

import static com.redbean0721.utils.ConfigManager.checkConfigFile;
import static com.redbean0721.utils.EnvFileManager.checkEnvFile;

public class Main {
    private static final Logger logger = LoggerFactory.getLogger(Main.class);

    public static void initBot(String TOKEN) {
        try {
            File configFile = new File("config.yml");
            Yaml yaml = new Yaml();
            Map<String, Object> map = yaml.load(new FileInputStream(configFile));

            Map<String, Object> botSetting = (Map<String, Object>) map.get("BotSetting");
            Map<String, Object> botStatus = (Map<String, Object>) botSetting.get("BotStatus");

            String activateType = (String) botStatus.get("Activate");
            String activateName = (String) botStatus.get("Name");
            String onlineStatus = (String) botSetting.get("OnlineStatus");

            Activity activity;
            System.out.println(activateType.toLowerCase());
            System.out.println(activateName);
            switch (activateType.toLowerCase()) {
                case "listening":
                    activity = Activity.listening(activateName);
                    System.out.println("listening");
                    break;
                case "playing":
                    activity = Activity.playing(activateName);
                    System.out.println("playing");
                    break;
                case "watching":
                    activity = Activity.watching(activateName);
                    System.out.println("watching");
                    break;
                default:
                    activity = Activity.playing("/help");
                    System.out.println("default");
                    break;
            }

            OnlineStatus status;
            System.out.println(onlineStatus.toLowerCase());
            switch (onlineStatus.toLowerCase()) {
                case "idle":
                    status = OnlineStatus.IDLE;
                    System.out.println("idle");
                    break;
                case "do_not_disturb":
                    status = OnlineStatus.DO_NOT_DISTURB;
                    System.out.println("do_not_disturb");
                    break;
                case "offline":
                    status = OnlineStatus.OFFLINE;
                    System.out.println("offline");
                    break;
                default:
                    status = OnlineStatus.ONLINE;
                    System.out.println("default");
                    break;
            }

            JDA jda = JDABuilder.createDefault(TOKEN)
                    .enableIntents(GatewayIntent.GUILD_MESSAGES)
                    .enableIntents(GatewayIntent.MESSAGE_CONTENT)
                    .enableIntents(GatewayIntent.GUILD_MEMBERS)
                    .setActivity(activity)
                    .setStatus(status)
                    .build();
            jda.awaitReady();
            logger.info("Logged in: {} | {}", jda.getSelfUser().getName(), jda.getSelfUser().getId());
            logger.info("Version: {}", map.get("Version"));
        } catch (InvalidTokenException e) {
            logger.error("The provided token is invalid!");
        } catch (InterruptedException e) {
            logger.error("An error occurred while initializing the bot.", e);
        } catch (FileNotFoundException e) {
            logger.error("config.yml is not found.", e);
        }
    }

    public static void main(String[] args) {
        checkEnvFile();
        checkConfigFile();
        Dotenv dotenv = Dotenv.load();
        initBot(dotenv.get("TOKEN"));
    }
}