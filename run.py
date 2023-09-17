#!/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, flash
import mysql.connector
import json

DEBUG = True
app = Flask(__name__)
app.config['SECRET_KEY'] = 'REAL'


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        red = float(request.form.get('Rendimentos tributáveis'))
        if red == float(0):
            red = float(0.0001)
        qtd_dep = int(request.form.get('Quantidade de dependentes'))
        ded_outras = float(request.form.get('Outras deduções'))

            
        vlr_dep = 189.59
        ded_dep = float(qtd_dep) * float(vlr_dep)
        desc_simp = 528.00

        pr1 = 1320.00
        pr2 = 1251.28
        pr3 = 1285.65
        pr4 = 7507.49 - pr1 - pr2 - pr3

        pr0p = 0.075
        pr1p = 0.075
        pr2p = 0.09
        pr3p = 0.12
        pr4p = 0.14

        a = float(red) * pr0p
        b = pr1 * pr1p
        c = b + (float(red) - pr1) * pr2p
        d = b + pr2 * pr2p
        e = d + (float(red) - pr1 - pr2) * pr3p
        f = d + (pr1 + pr2 + pr3 - pr1 - pr2) * pr3p
        g = f + (float(red) - pr1 - pr2 - pr3) * pr4p
        h = f + (7507.49 - pr1 - pr2 - pr3) * pr4p
                
        if float(red) <= pr1:
            ded_prev = round(a, 2)
        elif float(red) == pr1:
            ded_prev = round(b, 2)
        elif float(red) > 1320.01 and float(red) < 2571.29:
            ded_prev = round(c, 2)
        elif float(red) == 2571.29:
            ded_prev = round(d, 2)    
        elif float(red) > 2571.30 and float(red) < 3856.94:
            ded_prev = round(e, 2)
        elif float(red) == 3856.94:
            ded_prev = round(f, 2)    
        elif float(red) > 3856.95 and float(red) <= 7507.49:
            ded_prev = round(g, 2)
        elif float(red) > 7507.49:
            ded_prev = round(h, 2)

        
        total_ded = round((float(ded_prev) + float(ded_dep) + float(ded_outras)), 2)

        if total_ded >= desc_simp:
            base_calc = round((float(red) - float(total_ded)), 2)
        elif total_ded < desc_simp:
            base_calc = round((float(red) - float(desc_simp)), 2)
                
        if base_calc < 0:
            base_calc = 0.00
        
        fx1p = 0.0
        fx2p = 0.075
        fx3p = 0.15
        fx4p = 0.225
        fx5p = 0.275
        fx1 = 2112.00
        fx2 = 714.65
        fx3 = 924.40
        fx4 = 913.63
        fx5 = base_calc - fx1 - fx2 - fx3 - fx4
        ise_fx1 = 0
        pir_fx2 = fx1 * fx1p + (base_calc - fx1) * fx2p
        pir_fx3 = fx1 * fx1p + fx2 * fx2p + (base_calc - fx1 - fx2) * fx3p
        pir_fx4 = fx1 * fx1p + fx2 * fx2p + fx3 * fx3p + (base_calc - fx1 - fx2 - fx3) * fx4p
        pir_fx5 = fx1 * fx1p + fx2 * fx2p + fx3 * fx3p + fx4 * fx4p + (base_calc - fx1 - fx2 - fx3 - fx4) * fx5p

        if base_calc <= fx1:
            ir = round(ise_fx1, 2)
        elif base_calc <= (fx2 + fx1):
            ir = round(pir_fx2, 2)
        elif base_calc <= (fx3 + fx2 + fx1):
            ir = round(pir_fx3, 2)
        elif base_calc <= (fx4 + fx3 + fx2 + fx1):
            ir = round(pir_fx4, 2)
        elif base_calc <= (fx5 + fx4 + fx3 + fx2 + fx1) or base_calc > (fx5 + fx4 + fx3 + fx2 + fx1):
            ir = round(pir_fx5, 2)

        slr_liq = round((float(red) - float(ded_prev) - float(ir)), 2)

        perc_t = round((((float(ded_prev) + float(ir)) / float(red))*100), 2)

        perc_ir = round((float(ir) / float(red)*100), 2)

        perc_in = round((float(ded_prev) / float(red)*100), 2)

        return render_template ("result.html", r = red, td = total_ded, bc = base_calc, irp = ir, inss = ded_prev, sl = slr_liq, pt = perc_t, pi = perc_ir, pin = perc_in)
    return render_template ("home.html")

@app.route('/domestic', methods=['GET', 'POST'])
def domestic():
    if request.method == 'POST':
        red = float(request.form.get('Salário do(a) trabalhador(a)'))
        if red == float(0):
            red = float(0.0001)
        qtd_dep = int(request.form.get('Qtde de dependentes'))
        ded_outras = float(0)

            
        vlr_dep = 189.59
        ded_dep = float(qtd_dep) * float(vlr_dep)
        desc_simp = 528.00

        pr1 = 1320.00
        pr2 = 1251.28
        pr3 = 1285.65
        pr4 = 7507.49 - pr1 - pr2 - pr3

        pr0p = 0.075
        pr1p = 0.075
        pr2p = 0.09
        pr3p = 0.12
        pr4p = 0.14

        a = float(red) * pr0p
        b = pr1 * pr1p
        c = b + (float(red) - pr1) * pr2p
        d = b + pr2 * pr2p
        e = d + (float(red) - pr1 - pr2) * pr3p
        f = d + (pr1 + pr2 + pr3 - pr1 - pr2) * pr3p
        g = f + (float(red) - pr1 - pr2 - pr3) * pr4p
        h = f + (7507.49 - pr1 - pr2 - pr3) * pr4p
                
        if float(red) <= pr1:
            ded_prev = round(a, 2)
        elif float(red) == pr1:
            ded_prev = round(b, 2)
        elif float(red) > 1320.01 and float(red) < 2571.29:
            ded_prev = round(c, 2)
        elif float(red) == 2571.29:
            ded_prev = round(d, 2)    
        elif float(red) > 2571.30 and float(red) < 3856.94:
            ded_prev = round(e, 2)
        elif float(red) == 3856.94:
            ded_prev = round(f, 2)    
        elif float(red) > 3856.95 and float(red) <= 7507.49:
            ded_prev = round(g, 2)
        elif float(red) > 7507.49:
            ded_prev = round(h, 2)

        
        total_ded = round((float(ded_prev) + float(ded_dep) + float(ded_outras)), 2)

        if total_ded >= desc_simp:
            base_calc = round((float(red) - float(total_ded)), 2)
        elif total_ded < desc_simp:
            base_calc = round((float(red) - float(desc_simp)), 2)
                
        if base_calc < 0:
            base_calc = 0.00
        
        fx1p = 0.0
        fx2p = 0.075
        fx3p = 0.15
        fx4p = 0.225
        fx5p = 0.275
        fx1 = 2112.00
        fx2 = 714.65
        fx3 = 924.40
        fx4 = 913.63
        fx5 = base_calc - fx1 - fx2 - fx3 - fx4
        ise_fx1 = 0
        pir_fx2 = fx1 * fx1p + (base_calc - fx1) * fx2p
        pir_fx3 = fx1 * fx1p + fx2 * fx2p + (base_calc - fx1 - fx2) * fx3p
        pir_fx4 = fx1 * fx1p + fx2 * fx2p + fx3 * fx3p + (base_calc - fx1 - fx2 - fx3) * fx4p
        pir_fx5 = fx1 * fx1p + fx2 * fx2p + fx3 * fx3p + fx4 * fx4p + (base_calc - fx1 - fx2 - fx3 - fx4) * fx5p

        if base_calc <= fx1:
            ir = round(ise_fx1, 2)
        elif base_calc <= (fx2 + fx1):
            ir = round(pir_fx2, 2)
        elif base_calc <= (fx3 + fx2 + fx1):
            ir = round(pir_fx3, 2)
        elif base_calc <= (fx4 + fx3 + fx2 + fx1):
            ir = round(pir_fx4, 2)
        elif base_calc <= (fx5 + fx4 + fx3 + fx2 + fx1) or base_calc > (fx5 + fx4 + fx3 + fx2 + fx1):
            ir = round(pir_fx5, 2)

        cpp = round((float(red) * float(0.08)), 2)

        gilrat = round((float(red) * float(0.008)), 2)

        fgts = round((float(red) * float(0.08)), 2)

        mfgts = round((float(red) * float(0.032)), 2)

        tdae = round((float(ded_prev) + float(ir) + float(cpp) + float(gilrat) + float(fgts) + float(mfgts)), 2)

        temp = round((float(red) + float(cpp) + float(gilrat) + float(fgts) + float(mfgts)), 2)

        slr_liq = round((float(red) - float(ded_prev) - float(ir)), 2)

        perc_t = round((((float(ded_prev) + float(ir)) / float(red))*100), 2)

        perc_ir = round((float(ir) / float(red)*100), 2)

        perc_in = round((float(ded_prev) / float(red)*100), 2)

        return render_template ("result2.html", r = red, td = total_ded, bc = base_calc, irp = ir, inss = ded_prev, sl = slr_liq, cont = cpp, gil = gilrat, fg = fgts, mfg = mfgts, dae = tdae, totalemp = temp)
    
    return render_template ("domestic.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('username')
        senha = request.form.get('password')
        a = 'admin'
        b = '***'
        if email == a and senha == b:
            return render_template ("logado.html", l = email)
        else:
            flash('Usuário não cadastrado!')
            return redirect('/login')
    return render_template ("login.html")
    
@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
        
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='17081803',
        database='dados',
    )
    cursor = conexao.cursor()

    if request.method == 'POST':
        nome = (request.form.get('Nome'))
        email = (request.form.get('Email'))
        senha = (request.form.get('Senha'))
        perfil = (request.form.get('Usuário', 'Profissional'))

        comando = f'INSERT INTO cadastro (nome, email, senha, perfil) VALUES ("{nome}", "{email}", "{senha}", "{perfil}")'
        cursor.execute(comando)
        conexao.commit()
        
        cursor.close()
        conexao.close()

        return render_template ("cadastrado.html")
    return render_template ("cadastrar.html")

@app.route('/logado', methods=['GET', 'POST'])
def logado():

    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='17081803',
        database='dados',
    )
    cursor = conexao.cursor()

    if request.method == 'POST':
        
        controle = (request.form.get('Listar'))
                
        Listar = controle
       
        if controle == Listar:
        
            comando = f'SELECT * FROM cadastro'
            cursor.execute(comando)
            resultado = cursor.fetchall()

            cursor.close()
            conexao.close()

            return render_template ("listar.html", cadastro = resultado)
    return render_template ("logado.html")

@app.route('/listar', methods=['GET', 'POST'])
def listar():
        
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='17081803',
        database='dados',
    )
    cursor = conexao.cursor()

    if request.method == 'POST':
        nome = (request.form.get('Idexcluir'))
        
        comando = f'DELETE FROM cadastro WHERE id={nome}';
        cursor.execute(comando)
        conexao.commit()
        
        cursor.close()
        conexao.close()

        flash(f'Id {nome}, Cadastro excluido com sucesso!')
        return render_template ("excluido.html")
    return render_template ("listar.html")

if __name__ == '__main__':
        app.run()