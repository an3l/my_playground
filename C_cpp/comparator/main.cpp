#include <iostream>
#include <list>
#include <string>
#include <algorithm>

class Player
{
  public:
    int id;
    std::string name;
  public:
    Player(int id, std::string name):id(id), name(name){};
    bool operator <(const Player &a) const
    {
      return id<a.id;
    }
};
class PlayerFunctor
{
  public:
  // compare 2 objects using names
  bool operator()(const Player &a, const Player &b)
    {
      if(a.name == b.name)
        return a<b;
      return a.name<b.name;
    }
};

int main()
{
  std::list<Player> listOfPlayers={Player(42, "Anel"),
                       Player(22, "Minela"),
                       Player(1, "Sanel"),
                       Player(31, "Sanela"),
                       Player(17, "Anele"),
                       Player(32, "Anel")
                       };

  std::cout<<"Before sorting: \n";
  for(Player& p : listOfPlayers)
  {
    std::cout<<"Player id: "<<p.id<<" name: "<<p.name<<std::endl;
  }  
  // Sort list according the default criteria:
  listOfPlayers.sort();
  std::cout<<"After sorting by id (default operator <): \n";
  for(Player& p : listOfPlayers)
  {
    std::cout<<"Player id: "<<p.id<<" name: "<<p.name<<std::endl;
  }  

  // Sort list according the custom criteria , using functors (function objects):
  listOfPlayers.sort(PlayerFunctor());
  std::cout<<"After sorting by name and using custom function object: \n";
  for(Player& p : listOfPlayers)
  {
    std::cout<<"Player id: "<<p.id<<" name: "<<p.name<<std::endl;
  } 

  return 0;
}
