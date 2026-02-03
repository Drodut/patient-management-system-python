
import sqlite3

while True:


    print (f"||||| CLINICA VIDA MAIS |||||")
    print (f"")
    print (f"O que deseja ?")
    print (f"Digite '1' para cadastrar um novo paciente.")
    print (f"Digite '2' para busca, lista e estatísticas de pacientes cadastrados.")
    print (f"Digite '3' para iniciar ou cancelar o agendamento de um paciente.")
    print (f"Digite '4' para liberar o atendimento do paciente.")
    print (f"Digite '0' para encerrar.")
    print()

    entrada = input ("escolha uma opção: ")
            

    conn = sqlite3.connect ('teste.db')
    cursor = conn.cursor()

    cursor.execute(  """
        CREATE TABLE IF NOT EXISTS Pacientes (
            id INTEGER PRIMARY KEY, 
            nome TEXT NOT NULL,
            idade INTEGER,
            telefone INTEGER,
            doc INTEGER,
            pagamento INTEGER
            );
    """)

    cursor.execute( """
        CREATE TABLE IF NOT EXISTS Agendamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paciente_id INTEGER,
            hora INTEGER,
            data INTEGER,
            local TEXT NOT NULL,
            medico TEXT NOT NULL,
            FOREIGN KEY (paciente_id) REFERENCES Pacientes (id)
            );
    """)

    def adicionar_paciente(cursor): 
        nome = input("Digite o nome do paciente: ")
        idade = int(input("Digite a idade do paciente: "))
        telefone = int(input("Digite o telefone do paciente: "))
        doc = int(input("Digite o RG/CPF do paciente: "))
        pagamento = input("Digite '1' se o paciente ja efetuou o pagamento e '0' se ainda não foi realizado: ")
        if pagamento == "1":
            p = "Em dia."
        else:
            p = "Pendente."
        
        cursor.execute ("INSERT INTO Pacientes (nome, idade, telefone, doc, pagamento) VALUES (?, ?, ?, ?, ?)", (nome, idade, telefone, doc, pagamento))
        conn.commit()
        print (f"Paciente {nome} cadastrado com sucesso.")
        print()
          
    def agendar_consulta(cursor, id, nome):
        
        hora = input("Digite o HORÀRIO que o paciente poderá ser consultado: ")
        if hora > "20:00":
            print("Não há profíssionais disponiveis neste horário. (horário de atendimento das 06:00h até 20:00h).")
            agendar_consulta(cursor, id, nome)              
        elif hora < "06:00":
            print("Não há profíssionais disponiveis neste horário, (horário de atendimento das 06:00h até 20:00h).")
            agendar_consulta(cursor, id, nome)
        data = input("Digite a DATA que o paciente poderá ser consultado: ")
        local = input("Digite o consultório que o paciente será atendido: ")
        medico = input("Digite o nome do profissional que atenderá o paciente: ")
        cursor.execute ("INSERT INTO Agendamentos (id, hora, data, local, medico) VALUES (?, ?, ?, ?, ?)", (id, hora, data, local, medico))
        conn.commit()
        print (f"Agendamento concluído para {nome}.")
        print()
           
      
    if entrada == "0":
        print("Sistema encerrado.")
        break
        
    
    elif entrada == "1":
        print ("||| CADASTRO DE PACIENTE |||")
        adicionar_paciente(cursor)
        
    elif entrada == "2":
        print()
        print ("||| CADASTROS |||")
        print("Digite '1' para a lista completa de pacientes cadastrados.")
        print("Digite '2' para saber as estatísticas dos pacientes cadastrados.")
        print("Digite '3' para efetuar uma busca pelo nome de um paciente.")
        lista = input ("Escolha uma opção:")
        
        ###### PARTE DOS CADASTROS ###### 
    
    ###### LISTA DE PACIENTES ######
        if lista == "1":
            selecionar_paciente = "SELECT * FROM Pacientes"
            cursor.execute(selecionar_paciente)
            pacientes = cursor.fetchall()
            print()
            print ("||| LISTA DE CADASTRADOS |||")
            for paciente in pacientes:
                for paciente in pacientes:
                    id, nome, idade, telefone , doc, p = paciente
                    print(f"ID: {id} | Nome: {nome} | Idade: {idade} | Telefone: {telefone} | RG/CPF: {doc} | Pagamento: {p}." )        
                    print()
        ###### ESTATISTICAS ######         
        elif lista == "2":
            cursor.execute("SELECT COUNT(*), AVG(idade), MIN(idade), MAX(idade) FROM Pacientes")
            total, idade, min_idade, max_idade = cursor.fetchone()

            print("\n||| ESTATÍSTICAS DOS PACIENTES |||")
            print(f"Total de pacientes: {total}")
            if total > 0:
                print(f"Idade média: {idade:.1f}")
                print(f"Paciente mais jovem: {min_idade} anos")
                print(f"Paciente mais velho: {max_idade} anos")
                print()


        ###### BUSCA POR NOME ######
        elif lista == "3":
            nome_busca = input("Digite o nome que você deseja buscar: ")  
        
            cursor.execute("SELECT * FROM Pacientes WHERE nome LIKE ?", ('%' + nome_busca + '%',))
            resultados = cursor.fetchall()   
        
            if resultados:
                print("Pacientes encontrados:")
                for paciente in resultados:
                    id, nome, idade, telefone, doc = paciente
                    print(f"ID: {id} | Nome: {nome} | Idade: {idade} | Telefone: {telefone} | RG/CPF: {doc}")          
                    print()
            else:
                print(f"Nenhum paciente encontrado com o nome '{nome_busca}'.")
                print()
            
        conn.commit() 
        
        ##### AGENDAMENTO #######
    elif entrada == "3":
        print("Para agendar uma consulta digite '1', para cancelar uma consulta digite '2'.")
        agendar_cancelar = input("Digite sua resposta: ")
        if agendar_cancelar == "1":
            nome_consulta = input("insira o nome do paciente que deseja agendar uma consulta: ")   
            cursor.execute("SELECT * FROM Pacientes WHERE nome LIKE ?", ('%' + nome_consulta + '%',))
            consulta = cursor.fetchall()
            if consulta:
                print("Paciente encontrado:")
                for paciente in consulta:
                    id, nome, idade, telefone, doc, pagamento = paciente
                    print(f"ID: {id} | Nome: {nome} | Idade: {idade} | Telefone: {telefone} | RG/CPF: {doc}")
                    print()             
                    agendar_consulta(cursor, id, nome)
            else: 
                print("Não encontrado na lista de pacientes cadastrados.")
                print()
                
        elif agendar_cancelar == "2":
            nome_consulta = input("insira o nome do paciente que deseja cancelar uma consulta: ")
            cursor.execute("SELECT id, nome FROM Pacientes WHERE nome LIKE ?", ('%' + nome_consulta + '%',))
            paciente = cursor.fetchone()
            if not paciente:
                print("Paciente não encontrado.")
                print()
                
            paciente_id, nome = paciente
            
            # Buscar agendamento
            cursor.execute("SELECT * FROM Agendamentos WHERE paciente_id = ?", (paciente_id,))
            agendamento = cursor.fetchone()

            print(f"Tem certeza que deseja cancelar o agendamento de {nome}? Digite '1' para SIM, '2' para NÃO.")
            confirmar = input("Digite sua resposta: ")
            

            if confirmar == "1":
                cursor.execute("DELETE FROM Agendamentos WHERE paciente_id = ?", (paciente_id,))
                conn.commit()
                print(f"Agendamento cancelado para o paciente {nome}.")
                print()
            else:
                print("Cancelamento abortado.")
                print()
    ###### ATENDIMENTO #####
    
    elif entrada == "4":
        nome_consulta = input("insira o nome do paciente que deseja liberar o atendimento: ")
        cursor.execute("SELECT id, nome, idade, telefone, doc, pagamento FROM Pacientes WHERE nome LIKE ?", ('%' + nome_consulta + '%',))
        paciente = cursor.fetchone()
        print("É uma emergência ? '1' para sim, '2' se não. ")
        emergencia = input("insira sua resposta: ")
        
        #emergencia
        if emergencia == "1":
            id, nome, idade, telefone, doc, pagamento = paciente
            #verifica se tem documento ou pagamento
            if doc or pagamento :
                print(f"Paciente {nome} liberado para atendimento.")
                print()
    
        elif paciente: 
            id, nome, idade, telefone, doc, pagamento = paciente
            
            #verifica se tem doc
            if not doc:
                print (f"O paciente {nome} não possui RG/CPF cadastrado.")
                print()
                
            #verifica o pagamento
            elif pagamento == "0":
                print (f"O paciente {nome} não está com o pagamento em dia.") 
                print()
             
            #verifica agendamento       
            else:
                cursor.execute("SELECT * FROM Agendamentos WHERE id = ?", (id,))
                agendamento = cursor.fetchone()
            
                if  agendamento:
                    print(f"Paciente {nome} liberado para atendimento.")
                    print()
            
                else:
                    print(f"Paciente {nome} não tem agendamentos.") 
                    print()
        
        else:
            print("Paciente não encontrado.")   
            print()        
        
    else :
        print ("OPÇÂO INVALIDA.")
        print()
               
    conn.close()      
