import javax.crypto.*;
import javax.crypto.spec.SecretKeySpec;
import java.io.*;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.security.InvalidKeyException;
import java.security.NoSuchAlgorithmException;

//Portions of this code are inspired and from http://www.codejava.net/coding/file-encryption-and-decryption-simple-example
public class handleCryptography {

    /**
     * encryption method utilizing aes encryption to either encrypt or decrypt file
     * @param cipherMode 1 or 2 indicating whether to encrypt or decrypt
     * @param filepath String of where file is
     * @param key Secretkey passed in
     */
    protected void encryption(int cipherMode, String filepath, SecretKeySpec key){
        //2 = decrypt mode
        //1 encrypt mode
        try {
            byte[] data = null;
            Path path = Paths.get(filepath);
            try {
                data = Files.readAllBytes(path);
            } catch (IOException e) {
                e.printStackTrace();
            }
            assert data!= null;
            Cipher cipher = Cipher.getInstance("AES/ECB/PKCS5Padding"); //work in progress to CBC
            cipher.init(cipherMode, key);
            FileInputStream inputStream  = new FileInputStream(String.valueOf(Paths.get(filepath)));
            inputStream.read(data);
            byte[] outputBytes = cipher.doFinal(data);
            String fileName;
            if (cipherMode == 2) {
                fileName = filepath.substring(0, filepath.length() - 15)
                        + filepath.substring(filepath.length() - 4, filepath.length());
            }
            else{
                fileName = filepath.substring(0,filepath.length()-4).concat("(encrypted)")
                        + filepath.substring(filepath.length()-4, filepath.length());
            }
            File outputFile = new File(fileName);
            FileOutputStream outputStream = new FileOutputStream(outputFile);
            outputStream.write(outputBytes);
            inputStream.close();
            outputStream.close();
        } catch (InvalidKeyException | NoSuchPaddingException |
                NoSuchAlgorithmException | BadPaddingException |
                IllegalBlockSizeException | IOException e) {
            e.printStackTrace();
        }
    }
}