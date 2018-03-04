# Public good game with punishment stage (F&G 2000)

> Fehr, E. and Gachter, S., 2000. Cooperation and punishment in public goods experiments.
 American Economic Review, 90(4), pp.980-994.
 
 This is just a standard public good game with one additional stage: punishment.
 It uses an extra model called Punishment that stores the information about punishment tokens, who send it 
 (a link to Player's model), and who is the recipient of punishment (again a foreign key to Player's model).
 
 By default oTree does not show the information about other models than Player, Group, Subsession in admin, neither
 it exports this data. So you need to write your own export module, or to dump the content of corresponding punishment 
 records for each player. 
 
 Something like that should work (if we are inside `Player` model):
 
 ```python
    self.punishments_received.all().values('receiver__id_in_group',
                                          'receiver__contribution',
                                          'sender__id_in_group',
                                          'sender__contribution',
                                          'amount'
                                          )
```
 will result in a dictionary of receiver and sender identities, their contributions and the amount of punishment
 sent to the specific player:
 
 ```python

{'receiver__id_in_group': 1, 'receiver__contribution': 12, 
'sender__id_in_group': 2, 'sender__contribution': 2, 'amount': 4}, 
{'receiver__id_in_group': 1, 'receiver__contribution': 12, 
'sender__id_in_group': 3, 'sender__contribution': 4, 'amount': 0}
```
 
 In a similar manner you can get all punishment decisions of a sender by calling:
 ```python
    self.punishments_sent.all()
```
