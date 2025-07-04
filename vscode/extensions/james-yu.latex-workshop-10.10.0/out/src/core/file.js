"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.file = void 0;
exports.initialize = initialize;
const vscode = __importStar(require("vscode"));
const os = __importStar(require("os"));
const path = __importStar(require("path"));
const tmp = __importStar(require("tmp"));
const utils = __importStar(require("../utils/utils"));
const lw_1 = require("../lw");
const logger = lw_1.lw.log('File');
let extraTeXExts;
exports.file = {
    tmpDirPath: '',
    getOutDir,
    getLangId,
    getJobname,
    getBibPath,
    getPdfPath,
    getFlsPath,
    hasBinaryExt,
    hasTeXExt,
    hasLaTeXLangId,
    hasTeXLangId,
    hasBibLangId,
    hasDtxLangId,
    hasLaTeXWorkshopLangId,
    setTeXDirs,
    exists,
    read,
    kpsewhich,
    toUri
};
initialize();
function initialize() {
    exports.file.tmpDirPath = createTmpDir();
}
setExtraTeXExts();
lw_1.lw.onConfigChange('latex.extraExts', setExtraTeXExts);
function setExtraTeXExts() {
    extraTeXExts = vscode.workspace.getConfiguration('latex-workshop').get('latex.extraExts', []);
}
/**
 * Creates a temporary directory and returns its path as a string.
 *
 * This function utilizes the `tmp` library to create a temporary directory. The
 * `unsafeCleanup` option is enabled, ensuring that the directory and its
 * contents are removed even if there are open file handles. The function then
 * normalizes the directory path by replacing the system-specific path
 * separators with forward slashes, making it compatible across different
 * operating systems. In the event of an error, it captures the exception,
 * handles it using a custom error handler `handleTmpDirError`, and then
 * rethrows the error to be handled by the calling function.
 *
 * @returns {string} The normalized path of the created temporary directory.
 * @throws Will throw an error if the temporary directory creation fails.
 */
function createTmpDir() {
    try {
        return tmp.dirSync({ unsafeCleanup: true }).name.split(path.sep).join('/');
    }
    catch (error) {
        if (error instanceof Error) {
            handleTmpDirError(error);
        }
        throw error;
    }
}
/**
 * Handles errors related to the temporary directory.
 *
 * This function is responsible for dealing with errors that occur in the
 * process of creating or accessing the temporary directory used for building
 * TeX files. It checks if the temporary directory path contains single or
 * double quotes, which are not allowed. If such quotes are present, it logs an
 * error message and displays it to the user. Otherwise, it logs a generic error
 * message suggesting to check environment variables related to the temporary
 * directory paths.
 *
 * @param {Error} error - The error object encountered during the operation.
 */
function handleTmpDirError(error) {
    if (/['"]/.exec(os.tmpdir())) {
        const msg = `The path of tmpdir cannot include single quotes and double quotes: ${os.tmpdir()}`;
        void vscode.window.showErrorMessage(msg);
        logger.log(msg);
    }
    else {
        void vscode.window.showErrorMessage(`Error during making tmpdir to build TeX files: ${error.message}. Please check the environment variables, TEMP, TMP, and TMPDIR on your system.`);
        logger.log(`TEMP, TMP, and TMPDIR: ${JSON.stringify([process.env.TEMP, process.env.TMP, process.env.TMPDIR])}`);
    }
}
/**
 * Checks if the given file extension is associated with TeX-related extensions.
 *
 * This function verifies whether a provided file extension string matches any
 * of the TeX-related extensions defined in several constant arrays. It
 * consolidates these arrays into a single collection and checks if the given
 * extension exists within this collection. The arrays include TeX extensions
 * (including those defined by the user ), R Sweave extensions, Julia Weave extensions,
 * and Python Weave extensions.
 *
 * @param {string} extname - The file extension to be checked including the dot
 * (e.g., '.tex').
 * @returns {boolean} - Returns true if the extension is one of the TeX-related
 * extensions; otherwise, false.
 */
function hasTeXExt(extname) {
    return [
        ...extraTeXExts,
        ...lw_1.lw.constant.TEX_EXT,
        ...lw_1.lw.constant.RSWEAVE_EXT,
        ...lw_1.lw.constant.JLWEAVE_EXT,
        ...lw_1.lw.constant.PWEAVE_EXT
    ].includes(extname);
}
/**
 * Determines if the provided file extension is not one of the TeX source
 * extensions.
 *
 * This function evaluates the given file extension and checks it against a
 * predefined list of TeX source extensions such as `.tex`, `.ltx`, `.sty`,
 * `.cls`, `.fd`, `.aux`, `.bbl`, `.blg`, `.brf`, `.log`, `.out`, and R Sweave
 * extensions, Julia Weave extensions, Python Weave extensions and user defined
 * tex extensions. It returns `true` if the extension is not found in this list,
 * and `false` otherwise. This is useful for filtering out non-TeX files from a
 * collection of files.
 *
 * @param {string} extname - The file extension to be checked including the dot
 * (e.g., '.tex').
 * @returns {boolean} - Returns `true` if the extension is not one of the TeX
 * source extensions, `false` if it is.
 */
function hasBinaryExt(extname) {
    return ![
        ...extraTeXExts,
        ...lw_1.lw.constant.TEX_EXT,
        ...lw_1.lw.constant.TEX_NOCACHE_EXT,
        ...lw_1.lw.constant.RSWEAVE_EXT,
        ...lw_1.lw.constant.JLWEAVE_EXT,
        ...lw_1.lw.constant.PWEAVE_EXT
    ].includes(extname);
}
/**
 * Determines if the given language ID corresponds to a LaTeX-related language.
 *
 * @param {string} langId - The language identifier to check.
 * @returns {boolean} Returns `true` if `langId` is one of the LaTeX-related
 * language identifiers, otherwise `false`.
 */
function hasLaTeXLangId(langId) {
    return ['latex', 'context', 'latex-expl3', 'pweave', 'jlweave', 'rsweave'].includes(langId);
}
/**
 * Determines if the given language ID corresponds to a LaTeX-related language.
 *
 * @param {string} langId - The language identifier to check.
 * @returns {boolean} Returns `true` if `langId` is one of the LaTeX-related
 * language identifiers, otherwise `false`.
 */
function hasTeXLangId(langId) {
    return ['tex', 'latex-class', 'latex-package', 'doctex', 'doctex-installer'].includes(langId);
}
/**
 * Returns `true` if the language id is 'bibtex'.
 *
 * @param {string} langId - The language identifier.
 * @returns {boolean} - Indicates whether the language is BibTeX.
 */
function hasBibLangId(langId) {
    return langId === 'bibtex';
}
/**
 * Returns `true` if the language id is 'doctex'.
 *
 * @param {string} langId - The language identifier.
 * @returns {boolean} - Indicates whether the language is Doctex.
 */
function hasDtxLangId(langId) {
    return langId === 'doctex';
}
function hasLaTeXWorkshopLangId(langId) {
    return hasLaTeXLangId(langId) || hasTeXLangId(langId) || hasBibLangId(langId) || hasDtxLangId(langId);
}
/**
 * An object that stores the output and auxiliary directories for TeX files.
 *
 * The `texDirs` object is a dictionary where each key is a string representing
 * the path to a TeX file, and the value is an object containing optional paths
 * for the output directory (`out`) and auxiliary directory (`aux`). This
 * structure allows for easy management and retrieval of directory paths
 * associated with each TeX file. This is particularly useful in scenarios where
 * multiple TeX files are being compiled, and each needs to have specific
 * directories for its output and auxiliary files.
 *
 * @type {Object.<string, {out?: string, aux?: string}>}
 */
const texDirs = {};
/**
 * Sets the output and auxiliary files directory for a root TeX file.
 *
 * This function takes the path to a root TeX file and optional paths for the
 * output and auxiliary directories. If the provided TeX file path does not end
 * with the '.tex' extension, the function appends it. It then stores the output
 * and auxiliary directory paths in a global `texDirs` object, using the TeX
 * file path as the key.
 *
 * The function ensures that each TeX file has an associated output and
 * auxiliary directory, which can be useful for tracing the various files
 * generated during the TeX compilation process.
 *
 * @param {string} tex - The path to a root TeX file. If it doesn't end with
 * '.tex', the extension is appended.
 * @param {string} [out] - The corresponding output directory path. Optional.
 * @param {string} [aux] - The corresponding auxiliary directory path. Optional.
 */
function setTeXDirs(tex, out, aux) {
    if (!tex.endsWith('.tex')) {
        tex += '.tex';
    }
    texDirs[tex] = { out, aux };
}
/**
 * Determines the output directory for a given LaTeX file path.
 *
 * This function calculates the output directory where LaTeX compilation
 * artifacts will be stored. If a specific LaTeX file path is provided, the
 * function uses it to determine the output directory. Otherwise, it defaults to
 * using the root file path. The function handles various scenarios, such as
 * undefined paths and placeholder replacements, ensuring the output directory
 * is appropriately formatted and normalized.
 *
 * The process begins by checking if the provided LaTeX file path (`texPath`) is
 * defined; if not, it defaults to the root file path of the LaTeX workshop. If
 * both are undefined, it returns the current directory (`./`). The function
 * retrieves the configuration for the LaTeX workshop and extracts the output
 * directory setting. If the setting is not specified, it defaults to the
 * current directory (`./`). It then replaces placeholders within the output
 * directory path with appropriate values using a utility function.
 *
 * The function further checks if the output directory is specified as `%DIR%`
 * or `%DIR_W32%` and attempts to retrieve a custom output directory from a
 * cached directory mapping. If none is found, it normalizes and formats the
 * output directory path, ensuring it uses forward slashes and trims any
 * trailing slashes.
 *
 * @param {string} [texPath] - The path to the LaTeX file. If not provided, the
 * root file path is used.
 * @returns {string} The resolved output directory path.
 */
function getOutDir(texPath) {
    texPath = texPath ?? lw_1.lw.root.file.path;
    // rootFile is also undefined
    if (texPath === undefined) {
        return './';
    }
    const configuration = vscode.workspace.getConfiguration('latex-workshop', lw_1.lw.file.toUri(texPath));
    const outDir = configuration.get('latex.outDir') || './';
    const out = utils.replaceArgumentPlaceholders(texPath, exports.file.tmpDirPath)(outDir);
    let result = undefined;
    if (outDir === '%DIR%' || outDir === '%DIR_W32%') {
        result = texDirs[texPath]?.out;
    }
    result = result ?? path.normalize(out).replaceAll(path.sep, '/');
    if (result !== './' && result.endsWith('/')) {
        result = result.slice(0, -1);
    }
    return result;
}
/**
 * Returns the language identifier based on the file extension.
 *
 * This function takes a filename as an input and examines its extension to
 * determine the appropriate language identifier string. If the extension does
 * not match any of the predefined types, the function returns undefined.
 *
 * @param {string} filename - The name of the file.
 * @returns {string | undefined} - The language identifier.
 */
function getLangId(filename) {
    const ext = path.extname(filename).toLocaleLowerCase();
    if (ext === '.tex' || extraTeXExts.includes(ext)) {
        return 'latex';
    }
    else if (lw_1.lw.constant.PWEAVE_EXT.includes(ext)) {
        return 'pweave';
    }
    else if (lw_1.lw.constant.JLWEAVE_EXT.includes(ext)) {
        return 'jlweave';
    }
    else if (lw_1.lw.constant.RSWEAVE_EXT.includes(ext)) {
        return 'rsweave';
    }
    else if (ext === '.dtx') {
        return 'doctex';
    }
    else {
        return;
    }
}
/**
 * Retrieves the job name for a LaTeX file based on the provided file path.
 *
 * If a job name is found in the configuration 'latex.jobname', it is returned;
 * otherwise, the function derives the job name from the base name of the
 * provided file path (excluding the directory and file extension).
 *
 * @param {string} texPath - The file path of the LaTeX document.
 * @returns {string} - The job name for the LaTeX document, either from the
 * configuration or derived from the file name.
 */
function getJobname(texPath) {
    const jobname = vscode.workspace.getConfiguration('latex-workshop', lw_1.lw.file.toUri(texPath)).get('latex.jobname');
    return jobname || path.parse(texPath).name;
}
/**
 * Constructs the absolute path to the PDF file corresponding to a given TeX
 * file.
 *
 * This function takes the path to a TeX file and generates the path to the
 * resulting PDF file. It first determines the directory of the TeX file and
 * combines it with the output directory, which is retrieved using the
 * `getOutDir` function. Finally, it appends the base name of the job (derived
 * from the TeX file) with a `.pdf` extension.
 *
 * @param {string} texPath - The path to the TeX file.
 * @returns {string} - The absolute path to the corresponding PDF file.
 */
function getPdfPath(texPath) {
    return path.resolve(path.dirname(texPath), getOutDir(texPath), path.basename(`${getJobname(texPath)}.pdf`));
}
/**
 * Retrieves the .fls file path associated with a given .tex file.
 *
 * This function determines the file system path to the .fls file generated
 * during the compilation of a LaTeX document. It starts by identifying the root
 * directory and output directory of the provided .tex file. Using the job name
 * derived from the .tex file, it constructs the expected .fls file name. The
 * function first checks if this .fls file exists in the output directory; if
 * found, it returns this path. If not found, it then checks an auxiliary
 * directory (if specified) for the .fls file and returns the path if it exists.
 * If the .fls file is not found in either location, the function returns
 * `undefined`.
 *
 * @param {string} texPath - The file path to the .tex file for which the .fls
 * file path is to be determined.
 * @returns {Promise<string | undefined>} - The path to the .fls file if it exists, or
 * `undefined` if it does not.
 */
async function getFlsPath(texPath) {
    const rootDir = path.dirname(texPath);
    const outDir = getOutDir(texPath);
    const fileName = path.parse(getJobname(texPath)).name + '.fls';
    let flsFile = path.resolve(rootDir, path.join(outDir, fileName));
    if (await exists(flsFile)) {
        return flsFile;
    }
    flsFile = path.resolve(rootDir, texDirs[texPath]?.aux ?? '', fileName);
    return await exists(flsFile) ? flsFile : undefined;
}
/**
 * A cache object for storing resolved paths of LaTeX targets.
 *
 * This object stores the results of `kpsewhich` command executions, where each
 * key is a query string constructed from the target and its format, and the
 * corresponding value is the resolved path to the target. The cache helps in
 * avoiding redundant executions of the `kpsewhich` command by returning
 * previously computed results quickly.
 */
const kpsecache = {};
/**
 * Resolves the path to a given LaTeX target using the `kpsewhich` command.
 *
 * This function uses `kpsewhich` to find the path to a specified LaTeX target,
 * such as a .bib file. It first constructs the query string based on the target
 * and whether it is a bibliography file. If the result for this query is
 * already cached, it returns the cached value immediately. Otherwise, it
 * constructs the `kpsewhich` command and attempts to run it. If the command
 * executes successfully and returns a valid path, it caches this result and
 * returns the path. If the command fails or returns an error code, it logs the
 * error and returns `undefined`.
 *
 * @param {string} target - The LaTeX target to resolve, such as a file name.
 * @param {boolean} [isBib=false] - Indicates whether the target is a
 * bibliography file, default is false.
 * @returns {string | undefined} The resolved path to the target, or `undefined`
 * if resolution fails.
 */
function kpsewhich(target, isBib = false) {
    const query = (isBib ? '-format=.bib ' : '') + target;
    if (kpsecache[query]) {
        logger.log(`kpsewhich cache hit on ${query}: ${kpsecache[query]} .`);
        return kpsecache[query];
    }
    const command = vscode.workspace.getConfiguration('latex-workshop').get('kpsewhich.path');
    logger.log(`Calling ${command} to resolve ${query} .`);
    try {
        const args = isBib ? ['-format=.bib', target] : [target];
        const cwd = lw_1.lw.root.dir.path || vscode.workspace.workspaceFolders?.[0].uri.path;
        const kpsewhichReturn = lw_1.lw.external.sync(command, args, { cwd });
        if (kpsewhichReturn.status === 0) {
            let output = kpsewhichReturn.stdout.toString().replace(/\r?\n/, '');
            logger.log(`kpsewhich returned with '${output}'.`);
            if (output !== '') {
                if (!path.isAbsolute(output) && cwd) {
                    output = path.resolve(cwd, output);
                    logger.log(`kpsewhich resolved to '${output}'.`);
                }
                kpsecache[query] = output;
            }
            return output;
        }
        logger.log(`kpsewhich returned with non-zero code ${kpsewhichReturn.status}.`);
        return undefined;
    }
    catch (e) {
        logger.logError(`Calling ${command} on ${query} failed.`, e);
        return undefined;
    }
}
/**
 * Resolves the file paths for a given bibliography file based on the base
 * directory and configuration settings.
 *
 * This function first retrieves the configuration 'latex.bibDirs' to obtain
 * directories specified for bibliography files. It combines these directories
 * with the provided base directory to form a list of directories to search for
 * the bibliography file. Additionally, if the root directory of the LaTeX
 * project is available, it is prepended to the search list. Depending on
 * whether the bibliography file name includes wildcards, the function either
 * resolves it using a file glob or directly searches for the file. If the file
 * cannot be resolved, the function optionally attempts to locate it using the
 * `kpsewhich` tool if enabled in the configuration 'kpsewhich.bibtex.enabled'.
 * Finally, the resolved bibliography file path(s) are returned.
 *
 * @param {string} bib - The name of the bibliography file to resolve.
 * @param {string} baseDir - The base directory to start the search from.
 * @returns {string[]} An array containing the resolved file path(s) for the
 * bibliography file, or an empty array if the file could not be resolved.
 */
async function getBibPath(bib, baseDir) {
    const configuration = vscode.workspace.getConfiguration('latex-workshop');
    const bibDirs = configuration.get('latex.bibDirs');
    let searchDirs = [baseDir, ...bibDirs];
    // chapterbib requires to load the .bib file in every chapter using
    // the path relative to the rootDir
    if (lw_1.lw.root.dir.path) {
        searchDirs = [lw_1.lw.root.dir.path, ...searchDirs];
    }
    const bibPath = bib.includes('*') ? utils.resolveFileGlob(searchDirs, bib, '.bib') : await utils.resolveFile(searchDirs, bib, '.bib');
    if (bibPath === undefined || bibPath.length === 0) {
        if (configuration.get('kpsewhich.bibtex.enabled')) {
            const kpsePath = kpsewhich(bib, true);
            return kpsePath ? [kpsePath] : [];
        }
        else {
            logger.log(`Cannot resolve bib path: ${bib} .`);
            return [];
        }
    }
    if (os.platform() === 'win32') {
        // Normalize drive letters on Windows.
        return [bibPath].flat().map(p => p.replace(/^([a-zA-Z]):/, (_, p1) => p1.toLowerCase() + ':'));
    }
    else {
        return [bibPath].flat();
    }
}
async function read(filePathOrUri, raise) {
    try {
        if (filePathOrUri instanceof vscode.Uri) {
            return (await vscode.workspace.fs.readFile(filePathOrUri)).toString();
        }
        else {
            return (await vscode.workspace.fs.readFile(lw_1.lw.file.toUri(filePathOrUri))).toString();
        }
    }
    catch (err) {
        if (raise === undefined || raise === false) {
            return undefined;
        }
        throw err;
    }
}
/**
 * Checks if a file or directory exists at the given URI or path.
 *
 * This function accepts a URI object or a string representing a file path. If
 * the input is a string, it is converted to a file URI using
 * `lw.file.toUri()`. The function then attempts to retrieve the status of the
 * file or directory at the given URI using `stat()` of VS Code workspace file
 * system API. If the status retrieval is successful, the function returns the
 * file stat, which can also be used to indicate that the file or directory
 * exists. If an error occurs (e.g., the file or directory does not exist), the
 * function catches the error and returns `false`.
 *
 * @param {vscode.Uri | string} uri - The URI or file path to check for
 * existence.
 * @returns {Promise<boolean>} - A promise that resolves to `true` if the file
 * or directory exists, and `false` otherwise.
 */
async function exists(uri) {
    if (typeof (uri) === 'string') {
        uri = lw_1.lw.file.toUri(uri);
    }
    try {
        return await lw_1.lw.external.stat(uri);
    }
    catch {
        return false;
    }
}
/**
 * Converts a file path to a VS Code URI.
 *
 * @param {string} filePath - The file path to be converted.
 * @returns {vscode.Uri} - The corresponding VS Code URI.
 */
function toUri(filePath) {
    const scheme = vscode.workspace.workspaceFolders?.filter(folder => filePath?.startsWith(folder.uri.path))[0]?.uri.scheme ?? (lw_1.lw.extra.liveshare.isGuest() ? 'vsls' : 'file');
    // LiveShare guest sessions use the native path API, even though vsls uses POSIX paths
    // this is a workaround that removes the drive letter from the path
    if (scheme === 'vsls' && lw_1.lw.extra.liveshare.isGuest() && os.platform() === 'win32') {
        filePath = filePath.replace(/^\w:\\/, '\\');
    }
    return vscode.Uri.file(filePath).with({ scheme });
}
//# sourceMappingURL=file.js.map