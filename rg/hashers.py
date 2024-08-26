import collections
from django.utils.translation import gettext_noop as _
from django.contrib.auth.hashers import PBKDF2PasswordHasher, mask_hash
from django.utils.crypto import constant_time_compare


class PBKDF2WrappedSHA1PasswordHasher(PBKDF2PasswordHasher):
    """
    A subclass of PBKDF2PasswordHasher that uses SHA1 as the
    hash function inside PBKDF2, instead of the default SHA256.
    """
    algorithm = "pbkdf2_wrapped_sha1"

    def encode_sha1_hash(self, sha1_hash):
        """
        This method takes a SHA1 hash, a salt, and an iteration count,
        and turns them into a password hash for this hasher.
        """
        # We don't need to store the salt or the iteration count because
        # they're fixed.
        return sha1_hash

    def verify(self, password, encoded):
        """
        This method checks if the given password is correct. It does this
        by hashing the password and comparing it to the hashed value in
        encoded, so we need to override it.
        """
        # We don't need to check the algorithm or the salt, because
        # they're always the same.
        return constant_time_compare(encoded, self.encode(password))

    def safe_summary(self, encoded):
        """
        This method provides a safe summary of the user's password.
        """
        return collections.OrderedDict([
            (_('algorithm'), self.algorithm),
            (_('hash'), mask_hash(encoded, show=3)),
        ])
