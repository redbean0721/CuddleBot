package com.redbean0721.utils;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Paths;

public class ConfigManager {
    private static final Logger logger = LoggerFactory.getLogger(ConfigManager.class);

    public static void checkConfigFile() {
        File configFile = new File("config.yml");
        if (!configFile.exists() || configFile.isDirectory()) {
            try {
                InputStream inputStream = ConfigManager.class.getResourceAsStream("/config.yml");
                if (inputStream != null) {
                    Files.copy(inputStream, Paths.get("config.yml"));
                    inputStream.close();
                    logger.info("config.yml file is missing! A new config.yml file has been created.");
                } else {
                    logger.error("Default config.yml not found in resources!");
                }
            } catch (IOException e) {
                logger.error("An error occurred while creating the .env file.", e);
            }
        }
    }
}
