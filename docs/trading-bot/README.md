# Raspberry Pi Autonomous Trading Bot

A Raspberry Pi connected via Teltonika cellular modem runs the [SKA trading](https://github.com/quantiota/SKA-Binance-API) bot autonomously. The Pi connects to the SKA API over cellular, executes the trading loop, and writes the results. Claude Code reads each loop report, checks the
structural constants, improves the bot parameters, and restarts the loop — no human intervention required.
