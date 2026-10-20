// Copyright (C) Shigeyuki <http://patreon.com/Shigeyuki>
// License: GNU AGPL version 3 or later <http://www.gnu.org/licenses/agpl.html>
//
// convert_dict engine glue for the Anki Spell Checker add-on.
//
//  - conversion : "convert_dict.js" + "convert_dict.wasm" (Chromium
//                 convert_dict compiled to WASM)
//  - host       : Python via QWebChannel ("convertDictBridge")
//
// The input .dic/.aff files are passed in by Python as base64 strings (the
// same way the result is returned), and the wasm payload is embedded into the
// page as base64 and handed to the module as "wasmBinary", so the engine
// needs no local file server and no fetch() calls. A fresh module instance is
// created for every conversion so that the WASM memory is released between
// dictionaries.

"use strict";

class ConvertDictEngine {
    constructor(bridge) {
        this.bridge = bridge;
        this.factory = null;
        this.wasmBytes = null;
        this.ready = false;
    }

    // ------------------------------------------------------------------ utils
    static bytesToBase64(bytes) {
        const CHUNK = 0x8000;
        let binary = "";
        for (let i = 0; i < bytes.length; i += CHUNK) {
            binary += String.fromCharCode.apply(null, bytes.subarray(i, i + CHUNK));
        }
        return btoa(binary);
    }

    static base64ToBytes(base64Text) {
        const binary = atob(base64Text);
        const bytes = new Uint8Array(binary.length);
        for (let i = 0; i < binary.length; i++) {
            bytes[i] = binary.charCodeAt(i);
        }
        return bytes;
    }

    static readWasmBase64() {
        if (typeof globalThis.convertDictWasmBase64 === "string") {
            return globalThis.convertDictWasmBase64;
        }
        return "";
    }

    log(message) {
        try { this.bridge.onLog(String(message)); } catch (e) { console.log(message); }
    }

    fail(error) {
        let message = String(error);
        if (error && error.message) {
            message = error.message;
        }
        this.log("ERROR: " + message);
        try { this.bridge.onError(message); } catch (e) { console.error(message); }
    }

    // -------------------------------------------------------------- init
    async init() {
        if (this.ready) { return; }
        try {
            if (typeof createConvertDictModule === "undefined") {
                throw new Error("convert_dict.js could not be loaded");
            }
            const wasmBase64 = ConvertDictEngine.readWasmBase64();
            if (!wasmBase64) {
                throw new Error("the convert_dict wasm payload was not provided");
            }
            this.factory = createConvertDictModule;
            this.wasmBytes = ConvertDictEngine.base64ToBytes(wasmBase64);
            this.ready = true;
            this.bridge.onReady();
        } catch (e) {
            this.fail(e);
        }
    }

    // ------------------------------------------------------------ convert
    async convert(affBase64, dicBase64) {
        if (!this.ready) {
            this.fail(new Error("the engine is not ready"));
            return;
        }
        try {
            const module = await this.factory({
                noInitialRun: true,
                print: (text) => this.log(text),
                printErr: (text) => this.log(text),
                wasmBinary: this.wasmBytes,
            });

            const affBytes = ConvertDictEngine.base64ToBytes(affBase64);
            const dicBytes = ConvertDictEngine.base64ToBytes(dicBase64);

            try { module.FS.mkdir("/work"); } catch (e) { /* the directory already exists */ }
            module.FS.writeFile("/work/input.aff", affBytes);
            module.FS.writeFile("/work/input.dic", dicBytes);

            let exitStatus = null;
            try {
                exitStatus = module.callMain(["/work/input"]);
            } catch (error) {
                if (typeof error === "number") {
                    exitStatus = error;
                } else {
                    throw error;
                }
            }
            if (exitStatus !== null && exitStatus !== undefined && exitStatus !== 0) {
                throw new Error("convert_dict exited with status " + exitStatus);
            }

            const bdicBytes = module.FS.readFile("/work/input.bdic");
            this.bridge.onResult(ConvertDictEngine.bytesToBase64(bdicBytes));
        } catch (e) {
            this.fail(e);
        }
    }
}
