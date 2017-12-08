<?php

$books = array(
           array('https://leanpub.com/rprogramming',
                 'R Programming for Data Science'),
           array('https://leanpub.com/datastyle',
                 'The Elements of Data Analytic Style')
           );

for ($x = 0; $x <= sizeof($books)-1; $x++) {

    $file_string = file_get_contents_curl($books[$x][0]);

    $regex_pre = 
        '/<ul class=\'book-details-list\'>\n<li class=\'detail\'>\n';
    $regex_apre = '\n<p>Readers<\/p>/s';
    $regex_actual = '<span>(.*)<\/span>';
    $regex = $regex_pre.$regex_actual.$regex_apre;

    preg_match($regex,$file_string,$title);
    $downloads = $title[1];

    echo $downloads." ".$books[$x][1]."<br>";

}

function file_get_contents_curl($url) {
    $ch = curl_init();

    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
    curl_setopt($ch, CURLOPT_AUTOREFERER, TRUE);
    curl_setopt($ch, CURLOPT_HEADER, 0);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, TRUE);       

    $data = curl_exec($ch);
    curl_close($ch);

    return $data;
}

?>
