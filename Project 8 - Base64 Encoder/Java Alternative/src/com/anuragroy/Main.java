package com.anuragroy;

import java.nio.charset.StandardCharsets;
import java.util.Base64;
import java.util.Scanner;

public class Main {

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.println("Enter key: ");
        String key = sc.nextLine();
        System.out.println(encode(key));
    }

    private static String encode(String str) {
        Base64.Encoder encoder = Base64.getEncoder();
        byte[] encoded = encoder.encode(str.getBytes(StandardCharsets.UTF_8));
        return new String(encoded);
    }
}
