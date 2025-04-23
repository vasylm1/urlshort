<?php
/* YOURLS Configuration File */

// ** Site Options **
define( 'YOURLS_SITE', 'https://urlshort-lmgm.onrender.com' );
define( 'YOURLS_HOURS_OFFSET', 0 );
define( 'YOURLS_LANG', '' );

// ** Users and Passwords **
$yourls_user_passwords = array(
  'admin' => 'yourpassword' // Replace with secure one
);

// ** URL shortening settings **
define( 'YOURLS_URL_CONVERT', 36 );
define( 'YOURLS_PRIVATE', true );
define( 'YOURLS_UNIQUE_URLS', true );
define( 'YOURLS_COOKIEKEY', 'fpsiaxh863g7hdy6oaqkgkbl6rmdu4sa' );

// ** Database settings **
define( 'YOURLS_DB_USER', 'shortly_i1sw_user' );
define( 'YOURLS_DB_PASS', 'yFKiZMIjnlq0Rhl5MvBh0KuIJyLO82j2' );
define( 'YOURLS_DB_NAME', 'shortly_i1sw' );
define( 'YOURLS_DB_HOST', 'dpg-d04h23uuk2gs73bgtqd0-a' );
define( 'YOURLS_DB_DRIVER', 'pgsql' ); // ✅ PostgreSQL driver
define( 'YOURLS_DB_PREFIX', 'yourls_' );

define( 'YOURLS_DEBUG', true );
