#!/usr/bin/env python
'''
Autor: Iago Roger
Revisão e Finalização do Script: Gabriel Saw
'''

import os, sys, time

versao = '0.1'

def disk(): # EDITAR PARTIÇÕES NO DISCO RIGIDO
    os.system("clear")
    print("Crie 2 Partições\n")
    time.sleep(2)
    os.system("cfdisk /dev/sda")

def formata(): # FORMATA PARTIÇÕES NO DISCO RIGIDO
    os.system('mkfs.ext4 /dev/sda1')
    os.system('mkswap /dev/sda2')
    os.system('swapon /dev/sda2')

def mount(): # CRIA UM DIRETORIO E MOUNTA UMA UNIDADE NO DIRETORIO
    os.system('mkdir /mnt/funtoo')
    os.system('mount /dev/sda1 /mnt/funtoo')

def stage3(): # BAIXAR O STAGE3 
    print("""
    ========================================================================
    # Stage's                                                              #
    ========================================================================\n
    === Build	           === Description\t\n
    funtoo-current	       The most commonly-selected build of Funtoo Linux. Receives rapid updates and preferred by desktop users.
    \t\n
    funtoo-stable	       Emphasizes less-frequent package updates and trusted, reliable versions of packages over the latest versions.\t\n
    [!] Pressione '99' para voltar a Menu Principal\n""")
    opcao = str(input("Build Select: "))
    if opcao == 'funtoo-current':
        os.system("cd /mnt/funtoo")
        os.system('wget -c http://build.funtoo.org/funtoo-current/x86-64bit/generic_64/stage3-latest.tar.xz')
        os.system('tar xpf stage3-latest.tar.xz')
        #os.system('rm -r stage3-*.tar.xz')
        #os.system('rm -r /mnt/funtoo/usr/src/linux-debian-*')
    
    if opcao == 'funtoo-stable':
        os.system("cd /mnt/funtoo")
        os.system('wget -c http://build.funtoo.org/funtoo-stable/x86-64bit/generic_64/stage3-latest.tar.xz')
        os.system('tar xpf stag3-latest.tar.xz')
        #os.system('rm -r stage3-*.tar.xz')
        #os.system('rm -r /mnt/funtoo/usr/src/linux-debian-*')

    if opcao == '99':
        menu()

def chroot(): # MONTADO ARQUIVOS NESSESARIOS PARA O CHROOT
     os.system("mount -t proc none /mnt/funtoo/proc")
     os.system("mount --rbind /sys /mnt/funtoo/sys")
     os.system("mount --rbind /dev /mnt/funtoo/dev")
     os.system("cp -L /etc/resolv.conf /mnt/funtoo/etc")

def sync(): # SINCRONICAR O REPOSITORIO
    os.system("chroot /mnt/funtoo emerge --sync")

def fstab(): # EDITAR O FSTAB COM FORME AS PARTIÇÕES
    arq = open("/etc/fstab", 'w')
    arq.write(
    '/dev/sda1    /             ext4    noatime        0 1\n'
    '/dev/sda2    none          swap    sw             0 0\n')
    arq.close()

def timezone(): # DEFINIR O ESTADO
    os.system('chroot /mnt/funtoo ls /usr/share/zoneinfo/America')
    estado = str(input("Digite seu Estado Aqui: "))
    os.sysem("chroot /mnt/funtoo ln -sf /usr/share/zoneinfo/America/%s /etc/localtime" % (estado))

def make_cfg(): # CONFIGURAR O MAKE.CONF
    print("Digite o numero de processadores que aparecer")
    os.system('chroot /mnt/funtoo grep "processor" /proc/cpuinfo | wc -l')
    proc = int(input("Enter N°: "))
    arq = open('chroot /mnt/funtoo /etc/portage/make.conf', 'w')
    arq.write(
    'CFLAGS="-march=native -O2 -pipe"\n'
    'CXXFLAGS="${CFLAGS}"\n'
    'ACCEPT_KEYWORDS="~amd64\n'
    'MAKEOPTS="-j%i"\n' % (proc +1))
    arq.close()

def hostname(): # ADICIONAR O HOSTNAME USUARIO
    os.system("chroot /mnt/funtoo nano /etc/conf.d/hostname")

def idioma(): # ADCIONANDO UM IDIOMA AO SISTEMA
    os.system("chroot /mnt/funtoo echo LINGUAS=\"pt_BR\" >> /etc/make.conf")
    os.system("chroot /mnt/funtoo echo LINGUAGE=\"pt_BR\" >> /etc/make.conf")
    os.system("chroot /mnt/funtoo nano /etc/locale.gen")
    print ('ADD LANG="pt_BR.UTF=-8"')
    time.sleep(3)
    os.system("chroot /mnt/funtoo nano /etc/env.d/02locale")
    os.system("chroot /mnt/funtoo nano /etc/conf.d/keymaps")
    os.system("chroot /mnt/funtoo locale-gen")
    os.system("chroot /mnt/funtoo env-update && source /etc/profile")

def flavor(): # HABILITAR DE ADCIONAR FLAVOR'S
    def sub_menu(): # SUBMENU COM ALGUMAS DE'S
        print ('''
        ========================================================================
        # DE's                                                                 #
        ========================================================================\n
        1) Gnome
        2) Xfce
        3) Lxde
        4) Lxqt
        5) Kde\n
        X para sair\n''')
        resposta = int(input("Digite um Numero: "))
        if resposta == 1:
            os.system("chroot /mnt/funtoo eselect profile add funtoo/1.0/linux-gnu/mix-ins/gnome") # HABILITA O GNOME
        if resposta == 2:
            os.system("chroot /mnt/funtoo eselect profile add funtoo/1.0/linux-gnu/mix-ins/xfce") # HABILITA O XFCE
        if resposta == 3:
            os.system("chroot /mnt/funtoo eselect profile add funtoo/1.0/linux-gnu/mix-ins/lxde") # HABILITA O LXDE
        if resposta == 4:
            os.system("chroot /mnt/funtoo eselect profile add funtoo/1.0/linux-gnu/mix-ins/lxqt") # HABILIDA O LXQT
        if resposta == 5:
            os.system("chroot /mnt/funtoo eselect profile add funtoo/1.0/linux-gnu/mix-ins/kde") # HABILITA O KDE
        if resposta == 'x':
            sys.exit(1)

    os.system("clear")

    print ("\nTodos Profile Selecionados e Adicionados ao Sistema\n")
    os.system("chroot /mnt/funtoo eselect profile show") # MOSTRA TODOS OS FLAVOR'S HABILIDATOS E ADICIONADOS AO SISTEMA

    print ("Habilitado Flavor Desktop")
    time.sleep(2)
    os.system("chroot /mnt/funtoo eselect profile set-flavor funtoo/1.0/linux-gnu/flavor/desktop") # HABILITA O FLAVOR PARA DESKTOP
    enter = input("Pressione ENTER para selecionar a DE")
    if enter == '':
        sub_menu()

def kernel(): # BAIXA E COMPILA A KERNEL MAIS ESTAVEL
    os.system("chroot /mnt/funtoo emerge vanilla-sources")
    os.system("chroot /mnt/funtoo cd /usr/src/linux")
    #os.system("chroot /mnt/funtoo wget -c http://mirror.ic.ufmt.br/slackware/slackware64-current/testing/source/config-testing-4.1.1/config-huge-4.1.1.x64")
    #os.system("chroot /mnt/funtoo mv config-huge-*.x64 .config")
    func = input("Pressione ENTER para criar sua propria .config") # FUNCAO PARA CRIAR A PROPRIA CONFIGURACAO DA KERNEL
    if func == '':
        os.system("chroot /mnt/funtoo/ make menuconfig")
    os.system("chroot /mnt/funtoo make all")
    os.system("chroot /mnt/funtoo make modules_install")
    os.system("chroot /mnt/funtoo cp arch/x86/boot/bzImage /boot/kernel-4.x-FUNTOO")
    os.system("chroot /mnt/funtoo cd /boot && ls -l")
    os.system("chroot /mnt/funtoo ln -s kernel-4.x-FUNTOO bzImage")


def boot(): # BAIXA O BOOT-UPDATE UM PACOTE QUE CONTEM O GRUB E INSTALA
    os.system("chroot /mnt/funtoo emerge boot-update")
    os.system("chroot /mnt/funtoo grub-install --target=i386-pc --no-floppy --rechech --debug /dev/sda")
    os.system("chroot /mnt/funtoo boot-update")

def utm_ajustes():
    print ("O script instalarar ferramentas importates para o sistema funcionar\n")
    os.system("chroot /mnt/funtoo emerge dhcpcd syslog-ng cronie mlocate")
    os.system("chroot /mnt/funtoo rc-update add dhcpcd default")
    os.systsem("chroot /mnt/funtoo rc-update add syslog-ng default"
    os.system("chroot /mnt/funtoo rc-update add cronie default")
    os.system("chroot /mnt/funtoo emerge linux-firmware")
    
def passwd():
    print ("quando o sistema reinicinar você precisarar de uma senha.")
    os.system("chroot /mnt/funtoo passwd")

def user():
    print ("Defina um nome de usuario para o sistema. OBS: tem que ser com letra minuscula e sem numeros no inicio")
    otv = str(input("Digite seu nome aqui: "))
    os.system("chroot /mnt/funtoo useradd -m -g users -s /bin/bash %s" % (otv))
    print ("definir a senha do usuario")
    os.system("chroot /mnt/funtoo passwd %s" % (otv))
    
def final():
    print ("Ultios ajustes")
    os.system("cd /mnt")
    os.system("umount -l funtoo")
    os.system("reboot")
    
def menu(): # MENU PRINCIPAL
    print('''
    ========================================================================
    # Installation Funtoo                                      Versão: %s #
    ========================================================================\n
    1) Disco
    2) Formatação
    3) Montar as Partições
    4) Stage3
    5) Chroot
    6) Sync
    7) Fstab
    8) Timezone
    9) Make Config
    10) Hostname
    11) Idioma
    12) Flavor
    13) Kernel
    14) Boot
    15) Ultimos ajustes
    16) Definir senha
    17) Definir Usuario
    18) Final\n
    [!] Pressione '99' sair do Instalado\n''' % (versao))
    op = int(input("Escolhe Uma Opção: "))
    if op == 1:
        disk()
    if op == 2:
        formata()
    if op == 3:
        mount()
    if op == 4:
        stage3()
    if op == 5:
        chroot()
    if op == 6:
        sync()
    if op == 7:
        fstab()
    if op == 8:
        timezone()
    if op == 9:
        make_cfg()
    if op == 10:
        hostname()
    if op == 11:
        idioma()
    if op == 12:
        flavor()
    if op == 13:
        kernel()
    if op == 14:
        boot()
    if op == 15:
        utm_ajustes()
    if op == 16:
        passwd()
    if op == 17:
        user()
    if op == 18:
        final()
    if op == 99:
        exit()

    return menu()

if __name__ == '__main__':
    menu()

