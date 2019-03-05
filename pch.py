import os
import random
import weakref
import inspect

os.system('cls')

__string = ''

def printf(text, do_print=False):
    global __string
    __string += '{}\n'.format(text)
    if do_print:
        print(text)
        __string = ''

class Matsch():

    _instances = []
    id = 100

    def __init__(self, round):
        self.p1 = None
        self.p2 = None
        self.winner = None
        self.id = Matsch.id
        self.round = round
        self.done = False
        self._instances.append(self)
        Matsch.id += 1
    
    def get(self, key):
        if key == 'p1':
            return self.p1
        elif key == 'p2':
            return self.p2
        elif key == 'winner':
            return self.winner
        elif key == 'id':
            return self.id
        elif key == 'round':
            return self.round
        elif key == 'done':
            return self.done
        else:
            return None
    
    def __repr__(self):
        return self.__str__()
    
    def __str__(self):
        return "id:{} r:{} p:{}/{} : {}".format(self.id, self.round, self.p1, self.p2, self.winner)

    @staticmethod
    def objects(**kwargs):
        ret = []
        for cls in Matsch._instances:
            maybe = True
            for key, value in kwargs.items():
                if cls.get(key) != value:
                    maybe = False
            # printf('{} -> {}'.format(cls, maybe))
            if maybe:
                ret.append(cls)
        return ret
    
    def put_players_in_matsch(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
    
    def _return_players(self):
        return (self.p1, self.p2)
    
    def _return_winner(self):
        return self.winner
    
    def play_matsch(self, winner=None):
        if winner is not None:
            self.winner = winner
        else:
            self.winner = self.p1 if random.randint(0, 1) == 0 else self.p2
        self.done = True

class PCH():
    def __init__(self, nb_players, max_round):
        self.round = 0
        self.nb_players = nb_players
        self.max_round = max_round
        self.players = []
        self.forbiden_matsch = {}
        self.matsch_done = []
        self.matsch = []
    
    def put_players(self, players):
        self.players = players

    def build_forbiden_matsch(self):
        self.forbiden_matsch = {}
        for p in self.players:
            self.forbiden_matsch[p] = []
        for m in self.matsch_done:
            (p1, p2) = m._return_players()
            if p1 is not None:
                self.forbiden_matsch[p1].append(p2)
            if p2 is not None:
                self.forbiden_matsch[p2].append(p1)
        # printf(self.forbiden_matsch)

    def _show_actual_round(self):
        # printf(len(self.matsch))
        for m in self.matsch:
            printf(m)
    
    def _can_pair(self, o1, o2):
        if o1 in self.forbiden_matsch[o2]:
            return False
        if o2 in self.forbiden_matsch[o1]:
            return False
        return True
    
    def play_matsch(self):
        for m in self.matsch:
            m.play_matsch()
    
    def printf_score_players(self):
        sc, b, s = self.gimme_score(self.round)
        poeple_all_scores = []
        for player in self.players:
            poeple_all_scores.append((player, sc[player], b[player], s[player]))
        poeple_all_scores.sort(key=lambda t: t[1:], reverse=True)
        for p, scp, bp, sp in poeple_all_scores:
            f = ''
            for fm in self.forbiden_matsch[p]:
                f += '{}, '.format(fm)
            printf('{}: sc:{} b:{} s:{} f:[{}]'.format(p, scp, bp, sp, f))
    
    def gimme_score(self, round):
        b_score = {}
        s_score = {}
        score_player = {}

        for player in self.players:
            b_score[player] = 0
            s_score[player] = 0
            score_player[player] = 0
        
        for r in range(round):
            for m in Matsch.objects(round=r):
                (p1, p2) = m._return_players()
                if p1 is not None and p2 is not None:
                    b_score[p1] += score_player[p2]
                    b_score[p2] += score_player[p1]
                    if m._return_winner() == p1:
                        s_score[p1] += score_player[p2]
                        score_player[p1] += 2
                    elif m._return_winner() == p2:
                        s_score[p2] += score_player[p1]
                        score_player[p2] += 2
                    else:
                        s_score[p1] += int(0.5 * score_player[p2])
                        s_score[p2] += int(0.5 * score_player[p1])
                        score_player[p1] += 1
                        score_player[p2] += 1
        
        return score_player, b_score, s_score
    
    def make_round(self):
        for m in self.matsch:
            self.matsch_done.append(m)
        self.matsch = []
        self.build_forbiden_matsch()

        pairings = []
        removed = []

        score, b, s = self.gimme_score(self.round)
        poeple_all_scores = []
        for player in self.players:
            poeple_all_scores.append((player, score[player], b[player], s[player]))
        poeple_all_scores.sort(key=lambda t: t[1:], reverse=True)
        liste_score = {}
        # for p1, score, __, __ in people_all_scores

        if self.round == 0:
            half = int(len(self.players) / 2)
            pairings = zip(self.players[:half], self.players[half:])
            pairings = [(p1, p2) for p1, p2 in pairings]
        else:
            for p, s, __, __ in poeple_all_scores:
                if liste_score.get(s) is None:
                    liste_score[s] = [p]
                else:
                    liste_score[s].append(p)
            
            # scores = [k[0] for k in liste_score.items()]
            # scores.sort(reverse=True)

            def next_key(dic, key):
                key_list = [k for k in dic.keys()]
                if key_list.index(key) == len(key_list) - 1:
                    return None
                return key_list[key_list.index(key) + 1]

            printf(liste_score)
            for score, players in liste_score.items():
                half = int(len(players) / 2)
                if len(players) % 2 == 1:
                    player_to_change_group = players[-1]
                    nkey = next_key(liste_score, score)
                    # printf(score)
                    # printf(players)
                    liste_score[score].pop()
                    if nkey is None:
                        pairings.append((player_to_change_group, None))
                    else:
                        old = liste_score[nkey]
                        old = old[::-1]
                        old.append(player_to_change_group)
                        liste_score[nkey] = old[::-1]
                        # liste_score[nkey].append(player_to_change_group)
            for k, v in self.forbiden_matsch.items():
                printf('\t{}: {}'.format(k, v))
            printf(liste_score)
            for score, players in liste_score.items():
                half = int(len(players) / 2)
                split_1 = players[:half]
                split_2 = players[half:]

                check_order = [split_2, split_1]
                nkey = next_key(liste_score, score)
                while nkey is not None:
                    check_order.append(liste_score[nkey])
                    nkey = next_key(liste_score, nkey)
                    # printf(nkey)
                # for __, next_score_player in liste_score:
                #     check_order.append(next_score_player)
                for p1 in split_1:
                    printf(' t {:<10}'.format(p1))
                    if p1 in removed:
                        printf('!r {:<10}'.format(p1))
                        continue
                    
                    i_to_check = 0
                    pairing_done = False
                    while not pairing_done:
                        for p2 in check_order[i_to_check]:
                            printf(' w {:<10}'.format(p2))
                            if p2 in removed:
                                printf('!r {:<10}'.format(p2))
                                continue
                            if p1 == p2:
                                printf('!= {:<10} is   {:<10}'.format(p1, p2))
                                continue
                            if p2 in self.forbiden_matsch[p1]:
                                printf('!f {:<10} in   {:<10}'.format(p2, p1))
                                continue
                            if p1 in self.forbiden_matsch[p2]:
                                printf('!f {:<10} in   {:<10}'.format(p1, p2))
                                continue
                            pairings.append((p1, p2))
                            pairing_done = True
                            removed.append(p1)
                            removed.append(p2)
                            printf('+  {:<10}      {:<10}'.format(p1, p2))
                            break
                        
                        if pairing_done:
                            break
                        i_to_check += 1
                        if i_to_check >= len(check_order):
                            (op1, op2) = pairings[-1]
                            (p1, p2) = (removed[-1], removed[-2])
                            pairings.pop()
                            removed.pop()
                            removed.pop()
                            players = [op1, op2, p1, p2]
                            print(players)
                            if self._can_pair(op1, p2) and self._can_pair(p1, op2):
                                pairings.append((op1, p2))
                                pairings.append((p1, op2))
                                printf('+  {:<10}      {:<10}'.format(op1, p2))
                                printf('+  {:<10}      {:<10}'.format(p1, op2))
                                for i in [op1, op2, p1, p2]:
                                    removed.append(i)
                            elif self._can_pair(op1, p1) and self._can_pair(op2, p2):
                                pairings.append((op1, p1))
                                pairings.append((op2, p2))
                                printf('+  {:<10}      {:<10}'.format(op1, p1))
                                printf('+  {:<10}      {:<10}'.format(op2, p2))
                                for i in [op1, op2, p1, p2]:
                                    removed.append(i)
                            else: # C'est la merde
                                printf('#################################### r {} UNABLE TO PAIR {} ####################################'.format(self.round, p1), True)
                                not_not_done = False # = done
                                while not not_not_done:
                                    pass
                            break
        
        for p1, p2 in pairings:
            m = Matsch(self.round)
            m.put_players_in_matsch(p1, p2)
            self.matsch.append(m)
        self.round += 1


people = []
pch = PCH(32, 10)
tab = ["Adam","Adèle","Ahmed","Aïcha","Alban","Alex","Ali","Alix","Amel","Amélia","Amina","Amine","Anaëlle","Anastasia","Angélina","Antonin","Armand","Augustin","Bilal","Brahim","Candice","Capucine","Carla","Cassandre","Clarisse","Cloé","Cyprien","Dounia","Émile","Émilien","Farah","Fatoumata","Flora","Flore","Gabrielle","Giovanni","Hamza","Héléna","Héloïse","Ibrahim","Imane","Ismaël","Joseph","Julian","Justin","Laureen","Laury","Lolita","Lorenzo","Luca","Lucien","Mailys","Malik","Maria","Matthias","Maximilien","Mélina","Melvin","Moussa", "Emir","Elmire","Erol","Driss","Jamal","Hafida","Fahim","Faïrouz","Cémil","Béchir","Kaela","Bassem","Kadir","Jalil","Hadj","Fadila","Dima","Jalila","Hafid","Fahad","Barea","Almeria","Kadija","Jaïda","Ichem","Hadia","Gamal","Fadil","Baïa","Kader","Ibrahima","Hadi","Fadia","Badre","Abdeljalil","Lalia","Kacem","Bilal","Asma","Aménis","Amelle","Djamal","Fadi","Badis","Kaan","Jad","Hacène","Fadela","Daya","Dalil","Djibril","Hada","Faël","Jaber","Haby","Edris","Chirine","Cherine","Hamoud","Ilian","Arda","Camil","Assane","Badredine","Chafia","Alima","Hassina","Léonor","Keshia","Camel","Azzedine","Baya"]
for i in range(64):
    people.append(tab[(i * 8) % len(tab)])

pch.put_players(people)
for i in range(60):
    pch.make_round()
    pch.printf_score_players()
    pch.play_matsch()
    pch._show_actual_round()
    printf('-----------{:0>2}------------'.format(pch.round), True)

