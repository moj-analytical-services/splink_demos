<h1>Linking cluster IDs to cases in different snaphot dates</h1>

The text below originates from a [ASD Slack](asdslack.slack.com) [thread](https://asdslack.slack.com/archives/C01VDDG5V5W/p1643122229016000) where Robin Linacre 
([RobinL](https://github.com/RobinL)), Sam Linsday ([samnlinsday](https://github.com/samnlindsay)) and Ian Rickard (ian-rickard) explain how to correctly link 
`Splink` cluster IDs to cases in different snaphot dates.

Say you have XHIBIT defendant ID `X1`.  i.e. defendant id `X1` before any deduplication has taken place. `X1` is the primary key from the underlying operational 
database. (Defendant IDS are actually integers, we are just using `X1` as an example.)

Say we have a snapshot from `2019-01-01` and `2020-01-01`.

Maybe `X1` appears in only the cases from `2019-01-01`, and has been deleted from cases in `2020-01-01`.

Using the `Splink` linked data from `2020-01-01`, you can see that defendant ID `X1` is part of a cluster that contains, say, `X1`, `X2` and `X3`.  Let’s say 
that cluster has ID `splink_id_1`.

So you see cases in `2020-01-01` for `X2` and `X3`.

But you can link the cluster ID `splink_id_1` to _cases_ in **both** snapshot dates, because `splink_id_1` was derived from a fully completed list of *persons*. 

Which means that you can connect cases from `X1` in `2019-01-01` snapshot to cases from `X2` and `X3` in `2020-01-01` snapshot.

`X1`, `X2` and `X3` may be given `splink_id_1` in `2019-01-01` but then in `2020-01-01` they will remain in the same cluster but be given `splink_id_2`.

If you are creating a case table that splices together two snapshot dates there is a right and wrong way to proceed:

- **Wrong way**: 
  - Create a table of cases from `2019-01-10` with `Splink` IDs from `2019-01-01`. 
  - Create a second table of cases from `2020-01-01` with `Splink` IDs from `2020-01-01`. 
  - Vertically concatenate. 
  - Deduplicate table based on some identifiers of the case.
- **Right way**:  
  - Create a table of cases from `2019-01-01` and `2020-01-01` **WITHOUT** `Splink` IDs.
  - Vertically concatenate and deduplicate (i.e. remove repeated case rows).  
  - Then join on `Splink` IDs from the `2020-01-01` linked data product.

**In the "wrong way" you are mixing together** `Splink` **IDs from two snapshot dates, which you cannot do, because they are not stable between snapshot dates.**

**NOTE:** This means that new identity information  cannot change previously-determined shared cluster membership, i.e. say `Y1` and `Y2` are historically 
probabilistically identified as being the same individual. There is no way `Y3` comes along in the future and changes the balance of probabilities of shared 
identities to disrupt that (e.g. so that `Y2` and `Y3` are now thought to be the same person, but `Y1` is not that person). In other words, historical shared 
identities only unify with newer ones, they never disappear. Indeed, two previouly-distinct clusters may be joined by new information, but new information 
cannot split previously-joined clusters apart.
