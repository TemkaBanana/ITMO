#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <regex>
using namespace std;

bool isNumber( std::string token )
{
    return std::regex_match( token, std::regex( ( "((\\+|-)?[[:digit:]]+)(\\.(([[:digit:]]+)?))?" ) ) );
}

vector<string> split(const string& str, const string& delim) {
    vector<string> tokens;
    size_t prev = 0, pos = 0;
    do {
        pos = str.find(delim, prev);
        if (pos == string::npos) pos = str.length();
        string token = str.substr(prev, pos-prev);
        if (!token.empty()) tokens.push_back(token);
        prev = pos + delim.length();
    }
    while (pos < str.length() && prev < str.length());
    return tokens;
}

int main() {
  string line;
  long long summ = 0;
  ifstream myfile("nginx_logs");
  if (myfile.is_open()) {
    while (getline(myfile,line)) {
      vector<string> tokens = split(line, " ");
      if (isNumber(tokens[9])) {
        summ += stoi(tokens[9]);
      }
    }
    myfile.close();
  } else cout << "Unable to open file"; 

  cout << "Summ = " << summ << '\n';
  return 0;
}


