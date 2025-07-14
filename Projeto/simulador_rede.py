import networkx as nx
import ipaddress # Biblioteca padrão do Python para manipulação de endereços IP

class NetworkSimulator:
    def __init__(self):
        self.graph = nx.Graph()  # O grafo que representa a topologia da rede
        self.routing_tables = {} # Dicionário para armazenar as tabelas de roteamento de cada roteador
        self.ip_to_node_map = {} # Mapeia endereços IP para nós no grafo (ex: '192.168.0.1' -> 'host1')
        self.host_gateways = {} # Mapeia hosts para seus gateways padrão
        self.node_interfaces_and_subnets = {} # Mapeia roteadores para suas interfaces e as sub-redes às quais pertencem

    def load_network_configuration(self):
        """
        Etapa 2: Importe/defina a configuração da rede.
        Aqui self.graph, self.routing_tables e self.ip_to_node_map são populados
        com base na Tabela 1 fornecida e expansão das interfaces.
        """
        print("Carregando configuração da rede...")

        # 1. Adicionar nós (dispositivos) ao grafo
        # Definindo o tipo para cada nó
        self.graph.add_node('Core', type='router')
        self.graph.add_node('a1', type='router')
        self.graph.add_node('a2', type='router')
        self.graph.add_node('e1', type='router') # Switches de borda atuam como gateways/roteadores aqui
        self.graph.add_node('e2', type='router')
        self.graph.add_node('e3', type='router')
        self.graph.add_node('e4', type='router')
        self.graph.add_node('host1', type='host')
        self.graph.add_node('host2', type='host')
        self.graph.add_node('host3', type='host')
        self.graph.add_node('host4', type='host')
        self.graph.add_node('host5', type='host')
        self.graph.add_node('host6', type='host')
        self.graph.add_node('host7', type='host')
        self.graph.add_node('host8', type='host')

        # 2. Adicionar arestas (conexões) ao grafo
        # Você pode adicionar atributos como 'weight' (custo/distância), 'capacity', 'type' (fibra, par trançado)
        self.graph.add_edge('Core', 'a1', capacity='10Gbps', type='fibra_optica')
        self.graph.add_edge('Core', 'a2', capacity='10Gbps', type='fibra_optica')
        self.graph.add_edge('a1', 'e1', capacity='1Gbps', type='par_trancado_CAT6')
        self.graph.add_edge('a1', 'e2', capacity='1Gbps', type='par_trancado_CAT6')
        self.graph.add_edge('a2', 'e3', capacity='1Gbps', type='par_trancado_CAT6')
        self.graph.add_edge('a2', 'e4', capacity='1Gbps', type='par_trancado_CAT6')
        self.graph.add_edge('e1', 'host1', capacity='1Gbps', type='par_trancado_CAT6')
        self.graph.add_edge('e1', 'host2', capacity='1Gbps', type='par_trancado_CAT6')
        self.graph.add_edge('e2', 'host3', capacity='1Gbps', type='par_trancado_CAT6')
        self.graph.add_edge('e2', 'host4', capacity='1Gbps', type='par_trancado_CAT6')
        self.graph.add_edge('e3', 'host5', capacity='1Gbps', type='par_trancado_CAT6')
        self.graph.add_edge('e3', 'host6', capacity='1Gbps', type='par_trancado_CAT6')
        self.graph.add_edge('e4', 'host7', capacity='1Gbps', type='par_trancado_CAT6')
        self.graph.add_edge('e4', 'host8', capacity='1Gbps', type='par_trancado_CAT6')


        # 3. Mapear IPs para nomes dos nós (incluindo todas as interfaces dos roteadores)
        # IPs de hosts e gateways de borda (diretamente da sua Tabela 1)
        self.ip_to_node_map['192.168.0.1'] = 'host1'
        self.ip_to_node_map['192.168.0.2'] = 'host2'
        self.ip_to_node_map['192.168.0.3'] = 'e1' # Gateway da sub-rede e1
        self.ip_to_node_map['192.168.0.33'] = 'host3'
        self.ip_to_node_map['192.168.0.34'] = 'host4'
        self.ip_to_node_map['192.168.0.35'] = 'e2' # Gateway da sub-rede e2
        self.ip_to_node_map['192.168.0.65'] = 'host5'
        self.ip_to_node_map['192.168.0.66'] = 'host6'
        self.ip_to_node_map['192.168.0.67'] = 'e3' # Gateway da sub-rede e3
        self.ip_to_node_map['192.168.0.97'] = 'host7'
        self.ip_to_node_map['192.168.0.98'] = 'host8'
        self.ip_to_node_map['192.168.0.99'] = 'e4' # Gateway da sub-rede e4

        # IPs para interfaces dos links internos (baseado na expansão sugerida)
        # Core - a1 link (192.168.1.248/30)
        self.ip_to_node_map['192.168.1.249'] = 'Core'
        self.ip_to_node_map['192.168.1.250'] = 'a1'
        # Core - a2 link (192.168.1.252/30)
        self.ip_to_node_map['192.168.1.253'] = 'Core'
        self.ip_to_node_map['192.168.1.254'] = 'a2'
        # a1 - e1 link (192.168.0.128/30)
        self.ip_to_node_map['192.168.0.129'] = 'a1'
        self.ip_to_node_map['192.168.0.130'] = 'e1'
        # a1 - e2 link (192.168.0.132/30)
        self.ip_to_node_map['192.168.0.133'] = 'a1'
        self.ip_to_node_map['192.168.0.134'] = 'e2'
        # a2 - e3 link (192.168.0.136/30)
        self.ip_to_node_map['192.168.0.137'] = 'a2'
        self.ip_to_node_map['192.168.0.138'] = 'e3'
        # a2 - e4 link (192.168.0.140/30)
        self.ip_to_node_map['192.168.0.141'] = 'a2'
        self.ip_to_node_map['192.168.0.142'] = 'e4'

        print(f"Mapeamento IP-Nó: {self.ip_to_node_map}")

        # Populate self.node_interfaces_and_subnets
        # Isso mapeia cada roteador às suas interfaces e às sub-redes às quais pertencem.
        # É usado para determinar "diretamente conectado" para roteadores.
        self.node_interfaces_and_subnets = {
            'Core': {
                ipaddress.ip_address('192.168.1.249'): ipaddress.ip_network('192.168.1.248/30'),
                ipaddress.ip_address('192.168.1.253'): ipaddress.ip_network('192.168.1.252/30')
            },
            'a1': {
                ipaddress.ip_address('192.168.1.250'): ipaddress.ip_network('192.168.1.248/30'),
                ipaddress.ip_address('192.168.0.129'): ipaddress.ip_network('192.168.0.128/30'),
                ipaddress.ip_address('192.168.0.133'): ipaddress.ip_network('192.168.0.132/30')
            },
            'a2': {
                ipaddress.ip_address('192.168.1.254'): ipaddress.ip_network('192.168.1.252/30'),
                ipaddress.ip_address('192.168.0.137'): ipaddress.ip_network('192.168.0.136/30'),
                ipaddress.ip_address('192.168.0.141'): ipaddress.ip_network('192.168.0.140/30')
            },
            'e1': {
                ipaddress.ip_address('192.168.0.3'): ipaddress.ip_network('192.168.0.0/27'), # Rede de hosts e1
                ipaddress.ip_address('192.168.0.130'): ipaddress.ip_network('192.168.0.128/30') # Link e1-a1
            },
            'e2': {
                ipaddress.ip_address('192.168.0.35'): ipaddress.ip_network('192.168.0.32/27'), # Rede de hosts e2
                ipaddress.ip_address('192.168.0.134'): ipaddress.ip_network('192.168.0.132/30') # Link e2-a1
            },
            'e3': {
                ipaddress.ip_address('192.168.0.67'): ipaddress.ip_network('192.168.0.64/27'), # Rede de hosts e3
                ipaddress.ip_address('192.168.0.138'): ipaddress.ip_network('192.168.0.136/30') # Link e3-a2
            },
            'e4': {
                ipaddress.ip_address('192.168.0.99'): ipaddress.ip_network('192.168.0.96/27'), # Rede de hosts e4
                ipaddress.ip_address('192.168.0.142'): ipaddress.ip_network('192.168.0.140/30') # Link e4-a2
            }
        }
        # Hosts não precisam de entries aqui, pois sua lógica de roteamento é apenas usar o gateway.


        # 4. Carregar as tabelas de roteamento para cada roteador
        # Cada entrada da tabela de roteamento é um dicionário:
        # {'destination_network': 'rede/mascara', 'next_hop': 'IP_do_proximo_salto'}

        # Tabela de Roteamento: Core
        # O Core precisa conhecer todas as sub-redes de hosts (via a1 e a2)
        self.routing_tables['Core'] = [
            # Rotas para sub-redes de e1 e e2 (via a1)
            {'destination_network': '192.168.0.0/27', 'next_hop': '192.168.1.250'}, # IP da interface de a1 para Core
            {'destination_network': '192.168.0.32/27', 'next_hop': '192.168.1.250'}, # IP da interface de a1 para Core
            # Rotas para sub-redes de e3 e e4 (via a2)
            {'destination_network': '192.168.0.64/27', 'next_hop': '192.168.1.254'}, # IP da interface de a2 para Core
            {'destination_network': '192.168.0.96/27', 'next_hop': '192.168.1.254'}  # IP da interface de a2 para Core
        ]

        # Tabela de Roteamento: a1
        # a1 conhece suas redes diretas (e1, e2) E tem uma rota padrão para o Core
        self.routing_tables['a1'] = [
            # Rotas específicas para as sub-redes dos hosts abaixo de a1
            # Note: 192.168.0.0/27 já é diretamente conectada a e1. O next_hop para a1 é a interface de e1.
            {'destination_network': '192.168.0.0/27', 'next_hop': '192.168.0.130'}, # IP da interface de e1 para a1
            {'destination_network': '192.168.0.32/27', 'next_hop': '192.168.0.134'}, # IP da interface de e2 para a1
            # Rota Padrão para o Core (para qualquer outro tráfego)
            {'destination_network': '0.0.0.0/0', 'next_hop': '192.168.1.249'} # IP da interface de Core para a1
        ]

        # Tabela de Roteamento: a2
        # a2 conhece suas redes diretas (e3, e4) E tem uma rota padrão para o Core
        self.routing_tables['a2'] = [
            # Rotas específicas para as sub-redes dos hosts abaixo de a2
            {'destination_network': '192.168.0.64/27', 'next_hop': '192.168.0.138'}, # IP da interface de e3 para a2
            {'destination_network': '192.168.0.96/27', 'next_hop': '192.168.0.142'}, # IP da interface de e4 para a2
            # Rota Padrão para o Core (para qualquer outro tráfego)
            {'destination_network': '0.0.0.0/0', 'next_hop': '192.168.1.253'} # IP da interface de Core para a2
        ]

        # Tabela de Roteamento: e1, e2, e3, e4 (Switches de Borda)
        # Têm uma rota padrão para seus respectivos switches de agregação.
        # A lógica de "diretamente conectado" no _get_next_hop lidará com os hosts na mesma sub-rede.
        self.routing_tables['e1'] = [
            {'destination_network': '0.0.0.0/0', 'next_hop': '192.168.0.129'} # IP da interface de a1 para e1
        ]
        self.routing_tables['e2'] = [
            {'destination_network': '0.0.0.0/0', 'next_hop': '192.168.0.133'} # IP da interface de a1 para e2
        ]
        self.routing_tables['e3'] = [
            {'destination_network': '0.0.0.0/0', 'next_hop': '192.168.0.137'} # IP da interface de a2 para e3
        ]
        self.routing_tables['e4'] = [
            {'destination_network': '0.0.0.0/0', 'next_hop': '192.168.0.141'} # IP da interface de a2 para e4
        ]

        # Hosts não precisam de tabelas de roteamento complexas, apenas um gateway padrão.
        self.host_gateways = {
            'host1': '192.168.0.3', # Gateway e1
            'host2': '192.168.0.3', # Gateway e1
            'host3': '192.168.0.35', # Gateway e2
            'host4': '192.168.0.35', # Gateway e2
            'host5': '192.168.0.67', # Gateway e3
            'host6': '192.168.0.67', # Gateway e3
            'host7': '192.168.0.99', # Gateway e4
            'host8': '192.168.0.99', # Gateway e4
        }

        print("Tabelas de roteamento e mapeamento IP-Nó carregados.")
        
        # --- Prints de Diagnóstico na Inicialização ---
        print("\n--- Diagnóstico da Configuração Carregada ---")
        print(f" Interfaces e Sub-redes do e1: {self.node_interfaces_and_subnets.get('e1')}")
        print(f" Tabelas de Roteamento do e1: {self.routing_tables.get('e1')}")
        print(f" Interfaces e Sub-redes do a1: {self.node_interfaces_and_subnets.get('a1')}")
        print(f" Tabelas de Roteamento do a1: {self.routing_tables.get('a1')}")
        print(f" Tabelas de Roteamento do Core: {self.routing_tables.get('Core')}")
        print("-------------------------------------------\n")


    def get_node_by_ip(self, ip_address):
        """Retorna o nome do nó dado um endereço IP."""
        return self.ip_to_node_map.get(ip_address)

    def _get_next_hop(self, current_node_name, destination_ip_str):
        """
        Simula a lógica de roteamento para encontrar o próximo salto.
        Retorna o IP do próximo salto ou None se o destino for inalcançável.
        """
        destination_ip = ipaddress.ip_address(destination_ip_str)
        print(f"  [DEBUG] _get_next_hop: Nó atual={current_node_name}, Destino={destination_ip_str}")

        # 1. Se o nó atual for um HOST, ele encaminha para seu gateway padrão
        if self.graph.nodes[current_node_name]['type'] == 'host':
            gateway_ip = self.host_gateways.get(current_node_name)
            if gateway_ip:
                print(f"  [DEBUG] {current_node_name} (Host) encaminha para seu Gateway: {gateway_ip}")
                return gateway_ip
            print(f"  [DEBUG] {current_node_name} (Host) sem gateway definido.")
            return None # Host sem gateway

        # 2. Para ROTEADORES: Primeiro, verifica se o destino está em uma rede diretamente conectada
        if current_node_name in self.node_interfaces_and_subnets:
            print(f"  [DEBUG] {current_node_name} é um roteador. Verificando redes diretamente conectadas...")
            for interface_ip, connected_subnet in self.node_interfaces_and_subnets[current_node_name].items():
                print(f"    [DEBUG] Verificando interface {interface_ip} na sub-rede {connected_subnet}")
                if destination_ip in connected_subnet:
                    # Se o destino estiver em uma sub-rede diretamente conectada,
                    # o próximo salto é o próprio IP de destino.
                    # Isso simula a entrega local (ARP-like) dentro do segmento.
                    print(f"  [DEBUG] {current_node_name} (Router) Destino {destination_ip_str} na rede diretamente conectada {connected_subnet}. Próximo salto: {destination_ip_str}")
                    return destination_ip_str # Entregar diretamente
        
        print(f"  [DEBUG] {current_node_name}: Destino {destination_ip_str} NÃO está em uma rede diretamente conectada. Consultando tabela de roteamento...")
        # 3. Se não estiver diretamente conectado, busca na tabela de roteamento
        if current_node_name not in self.routing_tables:
            print(f"  [DEBUG] {current_node_name}: Não possui tabela de roteamento.")
            return None # Não tem tabela de roteamento

        best_match_next_hop = None
        longest_prefix_length = -1

        for entry in self.routing_tables[current_node_name]:
            dest_net = ipaddress.ip_network(entry['destination_network'])
            print(f"    [DEBUG] {current_node_name}: Avaliando rota para {dest_net} (pref: {dest_net.prefixlen}) via {entry['next_hop']}")
            if destination_ip in dest_net:
                if dest_net.prefixlen > longest_prefix_length:
                    longest_prefix_length = dest_net.prefixlen
                    best_match_next_hop = entry['next_hop']
                    print(f"      [DEBUG] {current_node_name}: Melhor match atualizado para {dest_net} via {best_match_next_hop} (pref: {longest_prefix_length})")
        
        if best_match_next_hop:
            print(f"  [DEBUG] {current_node_name}: Rota encontrada via match mais específico. Próximo salto: {best_match_next_hop}")
            return best_match_next_hop
        else:
            # Se não houver correspondência específica, tenta a rota padrão (0.0.0.0/0)
            print(f"  [DEBUG] {current_node_name}: Nenhuma rota específica encontrada. Tentando rota padrão...")
            for entry in self.routing_tables[current_node_name]:
                if entry['destination_network'] == '0.0.0.0/0':
                    print(f"  [DEBUG] {current_node_name}: Rota padrão encontrada. Próximo salto: {entry['next_hop']}")
                    return entry['next_hop']
        
        print(f"  [DEBUG] {current_node_name}: Nenhuma rota encontrada para {destination_ip_str}.")
        return None # Não encontrou rota

    def xping(self, source_ip, destination_ip):
        """
        Simula o comando Ping.
        Etapa 4: Faça xping no servidor/host remoto usando o comando Ping.
        Etapa 5: As estatísticas de pacotes do servidor xping são exibidas.
        """
        print(f"\n--- Executando xping de {source_ip} para {destination_ip} ---")
        source_node_name = self.get_node_by_ip(source_ip)
        destination_node_name = self.get_node_by_ip(destination_ip)

        if not source_node_name:
            print(f"Erro: Host de origem '{source_ip}' não encontrado na configuração da rede.")
            return
        if not destination_node_name:
            print(f"Erro: Host de destino '{destination_ip}' não encontrado na configuração da rede.")
            return

        print(f"Tentando ping de {source_node_name} para {destination_node_name}...")

        # Simula o pacote viajando pela rede
        current_node_name = source_node_name
        path = [current_node_name]
        ttl = 30 # Time To Live (TTL) - limite de saltos para evitar loops infinitos

        while current_node_name != destination_node_name and ttl > 0:
            print(f"\n[DEBUG] Saltando de {current_node_name} (TTL: {ttl})")
            next_hop_ip = self._get_next_hop(current_node_name, destination_ip)
            
            if not next_hop_ip:
                print(f"Destino inalcançável: Nenhuma rota encontrada de {current_node_name} para {destination_ip}.")
                print("Pacotes enviados: 4, Recebidos: 0, Perda: 100%")
                return
            
            # Descobre qual o nó correspondente ao next_hop_ip
            next_node_name = self.get_node_by_ip(next_hop_ip)
            if not next_node_name:
                # Este caso pode ocorrer se o next_hop_ip for o próprio destino_ip (entrega direta)
                if next_hop_ip == destination_ip:
                    next_node_name = destination_node_name # O próximo "nó" é o próprio destino final
                    print(f"[DEBUG] Próximo nó identificado como o destino final: {next_node_name}")
                else:
                    print(f"Erro: Próximo salto '{next_hop_ip}' não mapeado para um nó conhecido.")
                    print("Pacotes enviados: 4, Recebidos: 0, Perda: 100%")
                    return
            
            # Verifica se o link entre current_node_name e next_node_name existe no grafo
            # Exceção: Se o next_node_name for o próprio destino, e ele for um host,
            # não necessariamente há um 'link' no grafo para ele diretamente do roteador
            # se já estamos na sub-rede final.
            if next_node_name != destination_node_name and not self.graph.has_edge(current_node_name, next_node_name):
                 print(f"Erro: Link físico ausente entre {current_node_name} e {next_node_name}. Roteamento incorreto ou falha de conectividade física.")
                 print("Pacotes enviados: 4, Recebidos: 0, Perda: 100%")
                 return

            current_node_name = next_node_name
            path.append(current_node_name)
            ttl -= 1

        if current_node_name == destination_node_name:
            print(f"\nSucesso! Ping de {source_ip} para {destination_ip} bem-sucedido.")
            print(f"Caminho percorrido: {' -> '.join(path)}")
            print("Pacotes enviados: 4, Recebidos: 4, Perda: 0%")
            print("Tempo: Mínimo = Xms, Máximo = Yms, Média = Zms (simule tempos se necessário)")
        else:
            print(f"\nFalha! Destino não alcançado após {30 - ttl} saltos (TTL Expirado).")
            print("Pacotes enviados: 4, Recebidos: 0, Perda: 100%")

    def xtraceroute(self, source_ip, destination_ip):
        """
        Simula o comando Traceroute.
        Etapa 4: Mostre a rota para o servidor/host remoto usando o comando xtraceroute.
        Etapa 5: As estatísticas de comando xtraceroute são exibidas.
        """
        print(f"\n--- Executando xtraceroute de {source_ip} para {destination_ip} ---")
        source_node_name = self.get_node_by_ip(source_ip)
        destination_node_name = self.get_node_by_ip(destination_ip)

        if not source_node_name:
            print(f"Erro: Host de origem '{source_ip}' não encontrado na configuração da rede.")
            return
        if not destination_node_name:
            print(f"Erro: Host de destino '{destination_ip}' não encontrado na configuração da rede.")
            return

        print(f"Traçando rota de {source_node_name} para {destination_node_name}...")

        current_node_name = source_node_name
        hops = []
        ttl = 30 # Time To Live (TTL) para o traceroute

        while current_node_name != destination_node_name and ttl > 0:
            print(f"\n[DEBUG] Saltando de {current_node_name} (TTL: {ttl})")
            hops.append(current_node_name) # Adiciona o nó atual como um salto

            next_hop_ip = self._get_next_hop(current_node_name, destination_ip)
            if not next_hop_ip:
                hops.append("Destino Inalcançável (Nenhuma rota)")
                break
            
            next_node_name = self.get_node_by_ip(next_hop_ip)
            if not next_node_name:
                # Caso de entrega direta para um host (next_hop_ip é o destino_ip)
                if next_hop_ip == destination_ip:
                    next_node_name = destination_node_name
                    print(f"[DEBUG] Próximo nó identificado como o destino final: {next_node_name}")
                else:
                    hops.append(f"Próximo Salto Desconhecido ({next_hop_ip})")
                    break
            
            # Em um traceroute real, o IP mostrado é o da interface do roteador que respondeu.
            # Aqui, mostramos o nome do nó e o IP que ele usou para chegar ao próximo salto.
            
            # Verifica se o link existe (simulação de falha física)
            if next_node_name != destination_node_name and not self.graph.has_edge(current_node_name, next_node_name):
                 hops.append(f"Falha de Link para {next_node_name} (IP: {next_hop_ip})")
                 break

            current_node_name = next_node_name
            ttl -= 1
        
        if current_node_name == destination_node_name:
            hops.append(destination_node_name) # Adiciona o destino final se alcançado
            print("Rota:")
            for i, node in enumerate(hops):
                print(f"  {i+1} {node}")
            print(f"Traceroute completo. Saltos: {len(hops) - 1}")
        else:
            print("Rota:")
            for i, node in enumerate(hops):
                print(f"  {i+1} {node}")
            print(f"Destino inalcançável ou TTL expirado após {len(hops)} saltos.")


# --- Loop Principal da Aplicação ---
def main():
    simulator = NetworkSimulator()
    simulator.load_network_configuration() # Etapa 2: Importe/defina a configuração da rede.

    while True:
        print("\nComandos disponíveis:")
        print("1. xping <IP_ORIGEM> <IP_DESTINO>")
        print("2. xtraceroute <IP_ORIGEM> <IP_DESTINO>")
        print("3. listar_hosts (para ver os IPs disponíveis)")
        print("4. sair")

        command_line = input("Digite o comando: ").strip().split()
        command = command_line[0].lower()

        if command == 'xping' and len(command_line) == 3:
            source_ip = command_line[1]
            destination_ip = command_line[2]
            simulator.xping(source_ip, destination_ip)
        elif command == 'xtraceroute' and len(command_line) == 3:
            source_ip = command_line[1]
            destination_ip = command_line[2]
            simulator.xtraceroute(source_ip, destination_ip)
        elif command == 'listar_hosts':
            print("\nHosts e seus IPs:")
            for ip, node in simulator.ip_to_node_map.items():
                if node.startswith('host'):
                    print(f"  {node}: {ip}")
            # Exibir alguns IPs de interfaces de roteadores para testes
            print("\nIPs de Gateways e Interfaces de Roteadores para Teste de Roteamento:")
            print(f"  e1 (Gateway): 192.168.0.3")
            print(f"  e2 (Gateway): 192.168.0.35")
            print(f"  e3 (Gateway): 192.168.0.67")
            print(f"  e4 (Gateway): 192.168.0.99")
            print(f"  Core (link a1): 192.168.1.249")
            print(f"  Core (link a2): 192.168.1.253")
            print(f"  a1 (link Core): 192.168.1.250")
            print(f"  a1 (link e1): 192.168.0.129")
            print(f"  a1 (link e2): 192.168.0.133")
            print(f"  a2 (link Core): 192.168.1.254")
            print(f"  a2 (link e3): 192.168.0.137")
            print(f"  a2 (link e4): 192.168.0.141")


        elif command == 'sair':
            print("Saindo do simulador.")
            break
        else:
            print("Comando inválido. Por favor, tente novamente.")

if __name__ == "__main__":
    main()