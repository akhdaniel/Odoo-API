<?php
// https://github.com/akhdaniel/Odoo-API.git

$url = 'http://localhost:8069';
$db = '14ee';
$username = 'admin';
$password = '1';

require_once('ripcord/ripcord.php');
$common = ripcord::client("$url/xmlrpc/2/common");
$uid = $common->authenticate($db, $username, $password, array());

$models = ripcord::client("$url/xmlrpc/2/object");
$partner_ids = $models->execute_kw($db, $uid, $password, 'res.partner', 'search', array(array(array('is_company', '=', true))));

var_dump($partner_ids);
?>
