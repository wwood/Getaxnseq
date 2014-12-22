
import argparse
import re
import IPython
__author__ = "Joel Boyd"
__copyright__ = "Copyright 2014"
__credits__ = ["Joel Boyd"]
__license__ = "GPL3"
__maintainer__ = "Joel Boyd"
__email__ = "joel.boyd near uq.net.au"
__status__ = "Development"
__version__ = "0.0.1"

def main(arguments):
    
    Tax_n_Seq_builder().gg_taxonomy_builder(arguments.taxonomy)



class Tax_n_Seq_builder:
    
    def writer(self, levels , tax_ids):

        for level in levels['K']:
            tax_ids.append('%s,Root,kingdom,%s,%s,%s,,,,,,' % (level[0], level[0], 'Root', level[0]))

        for level in levels['P']:
            tax_ids.append('%s,%s,phylum,%s,%s,%s,%s,,,,,' % (level[1], level[0], level[1], 'Root', level[0], level[1])) 

        for level in levels['C']:
            tax_ids.append('%s,%s,class,%s,%s,%s,%s,%s,,,,' % (level[2], level[1], level[2], 'Root', level[0], level[1], level[2]))    

        for level in levels['O']:    
            tax_ids.append('%s,%s,order,%s,%s,%s,%s,%s,%s,,,' % (level[3], level[2], level[3], 'Root', level[0], level[1], level[2], level[3]))

        for level in levels['F']:
            tax_ids.append('%s,%s,family,%s,%s,%s,%s,%s,%s,%s,,' % (level[4], level[3], level[4], 'Root', level[0], level[1], level[2], level[3], level[4]))

        for level in levels['G']:
            tax_ids.append('%s,%s,genus,%s,%s,%s,%s,%s,%s,%s,%s,' % (level[5], level[4], level[5], 'Root', level[0], level[1], level[2], level[3], level[4], level[5]))   

        for level in levels['S']:
            tax_ids.append('%s,%s,species,%s,%s,%s,%s,%s,%s,%s,%s,%s' % (level[6], level[5], level[6], 'Root', level[0], level[1], level[2], level[3], level[4], level[5], level[6]))
            
        return tax_ids
    def gg_taxonomy_builder(self, taxonomy_file):
        
        levels = {'K' : [], 'P' : [], 'C' : [], 'O' : [], 'F' : [], 'G' : [], 'S' : []}
        tx = ['k__', 'd__', 'p__', 'c__', 'o__', 'f__', 'g__', 's__']
        tx2 = ['K', 'P', 'C', 'O', 'F', 'G', 'S']
        tax_ids = ['tax_id,parent_id,rank,tax_name,root,kingdom,phylum,class,order,family,genus,species', 'Root,Root,root,Root,Root,,,,,,,']
        sequence_ids = ['seqname,tax_id']
        
        for entry in open(taxonomy_file, 'r'):
            
            split = entry.rstrip().split('; ')
            
            tax_split = [split[0].split()[1]] + split[1:len(split)]
            
            for idx, item in enumerate(tax_split):
                tax_split[idx] = re.sub('\s+', '_', item)
            tax_split = [item for item in tax_split if item not in tx]
            
            sequence_ids.append(split[0].split().pop(0) + ',' + tax_split[len(tax_split)-1])           
            if tax_split not in levels[tx2[len(tax_split)-1]]:
                levels[tx2[len(tax_split)-1]].append(tax_split)  
                
                
    
        
        
        with open('Seq.csv', 'w') as seqout:
            
            for entry in sequence_ids:
                seqout.write(entry + '\n')
                
        
        tax_ids = Tax_n_Seq_builder().writer(levels,tax_ids)
        levels = {'K' : [], 'P' : [], 'C' : [], 'O' : [], 'F' : [], 'G' : [], 'S' : []}
        
        done = []
        unc = []
        parent = {}
        
        
        for i in tax_ids:
            if 'tax_id' not in i and not i.startswith('Root'):
                splt = [x for x in i.split(',') if x]
                done.append(splt[0])
                set_parent = set(parent)
                parenthood = splt[5:len(splt)-1]
                
                for idx, p in enumerate(parenthood):
                    if p not in set_parent:
                        
                        if p.startswith('d__'):
                            parent[p] = [p]
                        else:   
                            parent[p] = parenthood[0:idx+1]
                            
                
        
        set_done = set(done)
        
        for key, item in parent.iteritems():
            
            if key not in set_done:
                levels[tx2[len(item)-1]].append(item)
        
        
        tax_ids = Tax_n_Seq_builder().writer(levels,tax_ids)
        
        with open('Tax2.csv', 'w') as seqout:
            
            for entry in tax_ids:
                seqout.write(entry + '\n')
    

    
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='''Create a reference package %s''' % __version__
                                , epilog='==============================================================================')
    parser.add_argument('--taxonomy' ,type = str, help='Taxonomy file to be converted', required=True)
    args = parser.parse_args()

    main(args)  
