
<?php
/* YOURLS Configuration File */

// ** Site Options **
define( 'YOURLS_SITE', 'https://urlshort-lmgm.onrender.com' );
define( 'YOURLS_HOURS_OFFSET', 0 );
define( 'YOURLS_LANG', '' ); // Leave empty for English

// ** Users and Passwords **
// Username => password (plaintext or md5)
$yourls_user_passwords = array(
  'admin' => 'yourpassword'
);

// ** URL shortening settings **
define( 'YOURLS_URL_CONVERT', 36 );
define( 'YOURLS_PRIVATE', true );
define( 'YOURLS_UNIQUE_URLS', true );
define( 'YOURLS_COOKIEKEY', 'fpsiaxh863g7hdy6oaqkgkbl6rmdu4sa
' );

// ** Database settings **
define( 'YOURLS_DB_USER', 'root' );
define( 'YOURLS_DB_PASS', '' );
define( 'YOURLS_DB_NAME', 'yourls' );
define( 'YOURLS_DB_HOST', 'localhost' );
define( 'YOURLS_DB_PREFIX', 'yourls_' );

// Debug mode
define( 'YOURLS_DEBUG', false );
