from cryptography.fernet import Fernet

# To decrypt and save as plaintext file; specify file to decrypt, decrypted file destination, and key location
def decrypt(to_decrypt, file_destination, key_location):
    with open(key_location, 'rb') as f:
        key = f.read()
        
    fernet = Fernet(key)

    with open(to_decrypt, 'rb') as f:
        encrypted = f.read()

    decrypted = fernet.decrypt(encrypted)
    with open(file_destination, 'wb') as f:
        f.write(decrypted)


# Decrypt file; replace encrypted_filename.csv by filename
encrypted_filename = "anon_dataset_encrypted.csv"
decrypt(encrypted_filename, "decrypted_dataset.csv", "key.key")
