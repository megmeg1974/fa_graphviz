#!/usr/bin/env python3
# coding: utf-8


import re
from pprint import pprint
import sys

def sprint_dot(fa):

    ret =   ''

    ret +=  '''digraph G {
  graph [charset="UTF-8"];
  rankdir=LR;
'''
    
    ret +=  '  label="{title}";\n'.format(
            title=fa["title"])
    
    ret +=  "\n";
    
    def str_arrow(arrow):
        str_edge    =  "  {node1:<8} -> {node2:<8}".format(
                node1=arrow["node1"], node2=arrow["node2"])
        
        if  arrow["edge"]:
            str_atr =   ' [label="{edge}"];'.format(
                    edge=arrow["edge"]) if  arrow["edge"] else ""
            return str_edge + str_atr
        
        return str_edge
    
    ret +=  "\n".join(( str_arrow(arrow) for arrow in fa["arrows"] ))
    
    ret +=  "\n";
    
    for node    in  fa["final_nodes"]:
        ret += '  {node:<8} [shape=doublecircle rank=max];\n'.format(node=node)
    
    ret += '  {node:<8} [shape=none rank=max];\n'.format(node='start')

    ret +=  "}\n"

    return  ret

def get_node(txt):
    _match = re.compile('^([\w]+)\[F\]$').search(txt)
    if  _match:
        name    =   _match.group(1)
        is_final    =   True
    else:
        name    =   txt
        is_final    =   False
    
    return  {
        "name": name,
        "is_final": is_final,
    }
    
if __name__ == '__main__':
    if  len(sys.argv) > 1:
        in_file =   sys.argv[1]
    else:
        in_file =   './sample/sample_fa.txt'
    
    re_title    =   re.compile('^\s*title\s*:\s*(\S(?:.*\S)?)$')
    re_node_edge    =   re.compile('''
        ^\s*
        ([\w\[\]]+)                     # node1
        \s*
        -(?:([\w,\[\]]+)-|)>            # edge
        (                               # remain
            \s*
            ([\w\[\]]+)                 # node2
            (?:
                \s*
                -(?:[\w+,\[\]]-|)>
                \s*
                (?:[\w\[\]]+)
            )*
        )
        \s*$
        ''', re.VERBOSE)
    
    fa  =   {
        "title":'',
        "arrows":[],
        "final_nodes":[]
    }

    with open(in_file, 'r') as f:
        for line in ( l.rstrip() for l in f):
            if  re.compile('^\s*#').search(line):
                continue
            
            if  re.compile('^\s*$').search(line):
                continue

            _match = re_title.search(line)
            if  _match:
                fa["title"] =   _match.group(1)
                continue
            
            _line   =   line
            _match  =   re_node_edge.search(_line)
            if  _match:
                while   _match:
                    node1   =   get_node(_match.group(1))
                    edge    =   _match.group(2)
                    node2   =   get_node(_match.group(4))
                    _line   =   _match.group(3)
                    fa["arrows"].append({
                        "node1" :   node1["name"],
                        "edge"  :   edge,
                        "node2" :   node2["name"],
                    })
                    
                    for node in ( node for node in ( node1, node2 ) if node["is_final"]):
                        fa["final_nodes"].append(node["name"])
                    
                    _match  =   re_node_edge.search(_line)
                
                continue
    print(sprint_dot(fa))


