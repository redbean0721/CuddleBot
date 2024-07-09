package com.redbean0721.utils;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;

public class EnvFileManager {
    private static final Logger logger = LoggerFactory.getLogger(EnvFileManager.class);

    public static void checkEnvFile() {
        File envFile = new File(".env");
        if (!envFile.exists() || envFile.isDirectory()) {
            try {
                if (envFile.createNewFile()) {
                    try (FileWriter writer = new FileWriter(envFile)) {
                        writer.write("TOKEN=your_bot_token");
                        logger.error(".env file is missing!\n" +
                                "A new .env file has been created with a default token. Please update it with your actual Discord bot token.");
                    }
                }
            } catch (IOException e) {
                logger.error("An error occurred while creating the .env file.", e);
            }
            System.exit(1);
        }
    }
}
