from unittest import TestCase, mock

from etherscan.etherscan import Etherscan


class EtherscanTestCase(TestCase):
    def setUp(self):
        self.api = Etherscan(key="123test", plan="free")

    @mock.patch(
        "requests.get", return_value=mock.Mock(status_code=200, json=lambda: {})
    )
    def test_get(self, mock_get):
        self.api._get()
        mock_get.assert_called_once_with(
            url="https://api.etherscan.io/api",
            params={"apikey": self.api.key},
        )

    @mock.patch("etherscan.etherscan.logger.warning")
    @mock.patch(
        "requests.get",
        return_value=mock.Mock(
            status_code=404,
            json=lambda: {"message": "Not Found"},
            content=b"404 Not Found Message",
        ),
    )
    def test_get_404_status(self, mock_get, mock_log):
        with self.assertRaises(Exception) as context:
            self.api._get()
        self.assertEqual(
            "404 404 Not Found Message",
            str(context.exception),
        )
        mock_log.assert_called_once()

    @mock.patch("etherscan.etherscan.logger.info")
    @mock.patch(
        "requests.get",
        return_value=mock.Mock(
            status_code=404,
            json=mock.Mock(side_effect=Exception("")),
            content=b"404 Not Found Message",
        ),
    )
    def test_get_404_status_fail_silently(self, mock_get, mock_log):
        self.api.fail_silently = True
        self.assertEqual(self.api._get(), None)
        mock_log.assert_called_once()

    @mock.patch("etherscan.etherscan.Etherscan._get")
    def test_get_gas_oracle(self, mock_get):
        self.api.get_gas_oracle()
        mock_get.assert_called_once_with(
            params={"module": "gastracker", "action": "gasoracle"}
        )

    @mock.patch("etherscan.etherscan.Etherscan._get")
    def test_get_balance_single_address(self, mock_get):
        address = "0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae"
        tag = "latest"
        self.api.get_balance_single_address(address=address, tag=tag)
        mock_get.assert_called_once_with(
            params={
                "module": "account",
                "action": "balance",
                "address": address,
                "tag": tag,
            }
        )

    @mock.patch("etherscan.etherscan.Etherscan._get")
    def test_get_balance_multiple_addresses(self, mock_get):
        address = ["test1", "test2"]
        tag = "test"
        self.api.get_balance_multiple_addresses(address=address, tag=tag)
        mock_get.assert_called_once_with(
            params={
                "module": "account",
                "action": "balancemulti",
                "address": address,
                "tag": tag,
            }
        )

    @mock.patch("etherscan.etherscan.Etherscan._get")
    def test_get_normal_transactions_by_address(self, mock_get):
        address = "test"
        startblock = 1
        endblock = 2
        page = 1
        offset = 1
        sort = "asc"
        self.api.get_normal_transactions_by_address(
            address=address,
            startblock=startblock,
            endblock=endblock,
            page=page,
            offset=offset,
            sort=sort,
        )
        mock_get.assert_called_once_with(
            params={
                "module": "account",
                "action": "txlist",
                "address": address,
                "startblock": startblock,
                "endblock": endblock,
                "page": page,
                "offsetoffset": offset,
                "sort": sort,
            }
        )

    @mock.patch("etherscan.etherscan.Etherscan._get")
    def test_get_internal_transactions_by_address(self, mock_get):
        address = "test"
        startblock = 1
        endblock = 2
        page = 1
        offset = 1
        sort = "asc"
        self.api.get_internal_transactions_by_address(
            address=address,
            startblock=startblock,
            endblock=endblock,
            page=page,
            offset=offset,
            sort=sort,
        )
        mock_get.assert_called_once_with(
            params={
                "module": "account",
                "action": "txlistinternal",
                "address": address,
                "startblock": startblock,
                "endblock": endblock,
                "page": page,
                "offsetoffset": offset,
                "sort": sort,
            }
        )

    @mock.patch("etherscan.etherscan.Etherscan._get")
    def test_get_internal_transactions_by_hash(self, mock_get):
        txhash = "test"
        self.api.get_internal_transactions_by_hash(txhash=txhash)
        mock_get.assert_called_once_with(
            params={
                "module": "account",
                "action": "txlistinternal",
                "txhash": txhash,
            }
        )

    @mock.patch("etherscan.etherscan.Etherscan._get")
    def test_get_internal_transactions_by_block_range(self, mock_get):
        startblock = 1
        endblock = 2
        page = 1
        offset = 1
        sort = "asc"
        self.api.get_internal_transactions_by_block_range(
            startblock=startblock,
            endblock=endblock,
            page=page,
            offset=offset,
            sort=sort,
        )
        mock_get.assert_called_once_with(
            params={
                "module": "account",
                "action": "txlistinternal",
                "startblock": startblock,
                "endblock": endblock,
                "page": page,
                "offsetoffset": offset,
                "sort": sort,
            }
        )

    @mock.patch("etherscan.etherscan.Etherscan._get")
    def test_get_erc20_token_transferred_by_address(self, mock_get):
        address = "test"
        contractaddress = "test"
        page = 1
        offset = 1
        startblock = 1
        endblock = 1
        sort = "asc"
        self.api.get_erc20_token_transferred_by_address(
            address=address,
            contractaddress=contractaddress,
            page=page,
            offset=offset,
            startblock=startblock,
            endblock=endblock,
            sort=sort,
        )
        mock_get.assert_called_once_with(
            params={
                "module": "account",
                "action": "tokentx",
                "contractaddress": contractaddress,
                "address": address,
                "page": page,
                "offset": offset,
                "startblock": startblock,
                "endblock": endblock,
                "sort": sort,
            }
        )

    @mock.patch("etherscan.etherscan.Etherscan._get")
    def test_get_erc721_token_transferred_by_address(self, mock_get):
        address = "test"
        contractaddress = "test"
        page = 1
        offset = 1
        startblock = 1
        endblock = 1
        sort = "asc"
        self.api.get_erc721_token_transferred_by_address(
            address=address,
            contractaddress=contractaddress,
            page=page,
            offset=offset,
            startblock=startblock,
            endblock=endblock,
            sort=sort,
        )
        mock_get.assert_called_once_with(
            params={
                "module": "account",
                "action": "tokennfttx",
                "contractaddress": contractaddress,
                "address": address,
                "page": page,
                "offset": offset,
                "startblock": startblock,
                "endblock": endblock,
                "sort": sort,
            }
        )

    @mock.patch("etherscan.etherscan.Etherscan._get")
    def test_get_blocks_mined_by_address(self, mock_get):
        address = "test"
        blocktype = "test"
        page = 1
        offset = 1
        self.api.get_blocks_mined_by_address(
            address=address, blocktype=blocktype, page=page, offset=offset
        )
        mock_get.assert_called_once_with(
            params={
                "module": "account",
                "action": "getminedblocks",
                "address": address,
                "blocktype": blocktype,
                "page": page,
                "offset": offset,
            }
        )

    @mock.patch("etherscan.etherscan.Etherscan._get")
    def test_get_abi_verified_smart_contract(self, mock_get):
        address = "test"
        self.api.get_abi_verified_smart_contract(address=address)
        mock_get.assert_called_once_with(
            params={
                "module": "contract",
                "action": "getabi",
                "address": address,
            }
        )

    @mock.patch("etherscan.etherscan.Etherscan._get")
    def test_get_source_code_smart_contract(self, mock_get):
        address = "test"
        self.api.get_source_code_smart_contract(address=address)
        mock_get.assert_called_once_with(
            params={
                "module": "contract",
                "action": "getsourcecode",
                "address": address,
            }
        )

    @mock.patch("etherscan.etherscan.Etherscan._get")
    def test_get_contract_execution_status(self, mock_get):
        txhash = "test"
        self.api.get_contract_execution_status(txhash=txhash)
        mock_get.assert_called_once_with(
            params={
                "module": "transaction",
                "action": "getstatus",
                "txhash": txhash,
            }
        )

    @mock.patch("etherscan.etherscan.Etherscan._get")
    def test_get_transaction_execution_status(self, mock_get):
        txhash = "test"
        self.api.get_transaction_execution_status(txhash=txhash)
        mock_get.assert_called_once_with(
            params={
                "module": "transaction",
                "action": "gettxreceiptstatus",
                "txhash": txhash,
            }
        )

    @mock.patch("etherscan.etherscan.Etherscan._get")
    def test_get_block_uncleblock_reward_by_blockno(self, mock_get):
        blockno = 1
        self.api.get_block_uncleblock_reward_by_blockno(blockno=blockno)
        mock_get.assert_called_once_with(
            params={
                "module": "block",
                "action": "getblockreward",
                "blockno": blockno,
            }
        )

    @mock.patch("etherscan.etherscan.Etherscan._get")
    def test_get_estimate_mined_countdown_by_blockno(self, mock_get):
        blockno = 1
        self.api.get_estimate_mined_countdown_by_blockno(blockno=blockno)
        mock_get.assert_called_once_with(
            params={
                "module": "block",
                "action": "getblockcountdown",
                "blockno": blockno,
            }
        )

    @mock.patch("etherscan.etherscan.Etherscan._get")
    def test_get_block_number_by_tymestamp(self, mock_get):
        timestamp = 1
        self.api.get_block_number_by_tymestamp(timestamp=timestamp)
        mock_get.assert_called_once_with(
            params={
                "module": "block",
                "action": "getblocknobytime",
                "timestamp": timestamp,
            }
        )

    @mock.patch("etherscan.etherscan.Etherscan._get")
    def test_get_no_most_recent_block(self, mock_get):
        self.api.get_no_most_recent_block()
        mock_get.assert_called_once_with(
            params={"module": "proxy", "action": "eth_blockNumber"}
        )

    @mock.patch("etherscan.etherscan.Etherscan._get")
    def test_get_block_by_number(self, mock_get):
        tag = "test"
        boolean = True
        self.api.get_block_by_number(tag=tag, boolean=boolean)
        mock_get.assert_called_once_with(
            params={
                "module": "proxy",
                "action": "eth_getblockbynumber",
                "tag": tag,
                "boolean": boolean,
            }
        )

    @mock.patch("etherscan.etherscan.Etherscan._get")
    def test_get_uncle_by_block_number(self, mock_get):
        tag = "test"
        index = 1
        self.api.get_uncle_by_block_number(tag=tag, index=index)
        mock_get.assert_called_once_with(
            params={
                "module": "proxy",
                "action": "eth_getUncleByBlockNumberAndIndex",
                "tag": tag,
                "index": index,
            }
        )

    @mock.patch("etherscan.etherscan.Etherscan._get")
    def test_get_number_transaction_in_block(self, mock_get):
        tag = "test"
        self.api.get_number_transaction_in_block(tag=tag)
        mock_get.assert_called_with(
            params={
                "module": "proxy",
                "action": "eth_getBlockTransactionCountByNumber",
                "tag": tag,
            }
        )

    @mock.patch("etherscan.etherscan.Etherscan._get")
    def test_get_transaction_by_hash(self, mock_get):
        txhash = "test"
        self.api.get_transaction_by_hash(txhash=txhash)
        mock_get.assert_called_once_with(
            params={
                "module": "proxy",
                "action": "eth_getTransactionByHash",
                "txhash": txhash,
            }
        )

    @mock.patch("etherscan.etherscan.Etherscan._get")
    def test_get_transaction_by_blocknumber_and_index(self, mock_get):
        tag = "test"
        index = 1
        self.api.get_transaction_by_blocknumber_and_index(tag=tag, index=index)
        mock_get.assert_called_once_with(
            params={
                "module": "proxy",
                "action": "eth_getTransactionByBlockNumberAndIndex",
                "tag": tag,
                "index": index,
            }
        )

    @mock.patch("etherscan.etherscan.Etherscan._get")
    def test_get_count_transactions_by_address(self, mock_get):
        address = "test"
        tag = "test"
        self.api.get_count_transactions_by_address(address=address, tag=tag)
        mock_get.assert_called_once_with(
            params={
                "module": "proxy",
                "action": "eth_getTransactionCount",
                "address": address,
                "tag": tag,
            }
        )

    @mock.patch("etherscan.etherscan.Etherscan._get")
    def test_get_receipt_by_transaction_hash(self, mock_get):
        txhash = "test"
        self.api.get_receipt_by_transaction_hash(txhash=txhash)
        mock_get.assert_called_once_with(
            params={
                "module": "proxy",
                "action": "eth_getTransactionReceipt",
                "txhash": txhash,
            }
        )

    @mock.patch("etherscan.etherscan.Etherscan._get")
    def test_get_gas_price(self, mock_get):
        self.api.get_gas_price()
        mock_get.assert_called_once_with(
            params={"module": "proxy", "action": "eth_gasPrice"}
        )

    @mock.patch("etherscan.etherscan.Etherscan._get")
    def test_get_erc20_in_circulation(self, mock_get):
        contractaddress = "test"
        self.api.get_erc20_in_circulation(contractaddress=contractaddress)
        mock_get.assert_called_once_with(
            params={
                "module": "stats",
                "action": "tokensupply",
                "contractaddress": contractaddress,
            }
        )

    @mock.patch("etherscan.etherscan.Etherscan._get")
    def test_get_erc20_balance_of_address(self, mock_get):
        contractaddress = "test"
        address = "test"
        self.api.get_erc20_balance_of_address(
            contractaddress=contractaddress, address=address
        )
        mock_get.assert_called_once_with(
            params={
                "module": "stats",
                "action": "tokenbalance",
                "contractaddress": contractaddress,
                "address": address,
            }
        )

    @mock.patch("etherscan.etherscan.Etherscan._get")
    def test_get_ether_supply(self, mock_get):
        self.api.get_ether_supply()
        mock_get.assert_called_once_with(
            params={"module": "stats", "action": "ethsupply"}
        )

    @mock.patch("etherscan.etherscan.Etherscan._get")
    def test_get_eth2_supply(self, mock_get):
        self.api.get_eth2_supply()
        mock_get.assert_called_once_with(
            params={"module": "stats", "action": "ethsupply2"}
        )

    @mock.patch("etherscan.etherscan.Etherscan._get")
    def test_get_ether_last_price(self, mock_get):
        self.api.get_ether_last_price()
        mock_get.assert_called_once_with(
            params={"module": "stats", "action": "ethprice"}
        )

    @mock.patch("etherscan.etherscan.Etherscan._get")
    def test_get_nodes_size(self, mock_get):
        startdate = "test"
        enddate = "test"
        clienttype = "test"
        syncmode = "test"
        sort = "test"
        self.api.get_nodes_size(
            startdate=startdate,
            enddate=enddate,
            clienttype=clienttype,
            syncmode=syncmode,
            sort=sort,
        )
        mock_get.assert_called_once_with(
            params={
                "module": "stats",
                "action": "chainsize",
                "startdate": startdate,
                "enddate": enddate,
                "clienttype": clienttype,
                "syncmode": syncmode,
                "sort": sort,
            }
        )

    @mock.patch("etherscan.etherscan.Etherscan._get")
    def test_get_total_nodes_count(self, mock_get):
        self.api.get_total_nodes_count()
        mock_get.assert_called_once_with(
            params={"module": "stats", "action": "nodecount"}
        )
