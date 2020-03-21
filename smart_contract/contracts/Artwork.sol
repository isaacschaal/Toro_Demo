pragma solidity ^0.5.0;

import "./TradeableERC721Token.sol";
import "openzeppelin-solidity/contracts/ownership/Ownable.sol";

/**
 * @title Artwork
 * Artwork - a contract for my non-fungible artworks.
 */
contract Artwork is TradeableERC721Token {
  constructor(address _proxyRegistryAddress) TradeableERC721Token("Artwork", "AAI", _proxyRegistryAddress) public {  }

  function baseTokenURI() public view returns (string memory) {
    return "https://raw.githubusercontent.com/isaacschaal/metadata_hosting/master/";
    // The base url for the metadata
  }
}
