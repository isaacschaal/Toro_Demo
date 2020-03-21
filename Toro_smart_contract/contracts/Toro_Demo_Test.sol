pragma solidity ^0.5.0;

import "./TradeableERC721Token.sol";
import "openzeppelin-solidity/contracts/ownership/Ownable.sol";

/**
 * @title Toro_Demo_Test
 * Toro_Demo_Test - a contract to demo the capability of
 * minting artworks made by Toro.
 */
contract Toro_Demo_Test is TradeableERC721Token {
  constructor(address _proxyRegistryAddress) TradeableERC721Token("Toro_Demo_Test", "TDT", _proxyRegistryAddress) public {  }

  function baseTokenURI() public view returns (string memory) {
    return "https://raw.githubusercontent.com/isaacschaal/metadata_hosting/master/";
    // The base url for the metadata
  }
}
