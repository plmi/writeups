<?php
  $alphabet = "abcdefghijklmnopqrstuvwxyz012345679";

  function brute_variable_length($password, $depth) {
    for ($i = 1; $i <= $depth; ++$i) {
      brute_fixed_length("", 0, $i);
    }
  }

  function brute_fixed_length($password, $position, $size) {
		global $alphabet;
		if ($position < $size) {
			foreach (str_split($alphabet) as $c) {
				brute_fixed_length($password . $c, $position + 1, $size);
			}
    } else {
      $hash = hash('tiger128,4', $password);
      if ($hash == "0e132798983807237937411964085731") {
				echo "[+] " . $password . ":" . $hash . "\n";
      }
    }
  }

  brute_variable_length("", 8);
?>
