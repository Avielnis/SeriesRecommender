// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
const vscode = require('vscode');
const {spawn} = require('child_process');

// This method is called when your extension is activated
// Your extension is activated the very first time the command is executed

/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {

	// Use the console to output diagnostic information (console.log) and errors (console.error)
	// This line of code will only be executed once when your extension is activated
	console.log('Congratulations, your extension "codedescriber" is now active!');

	// The command has been defined in the package.json file
	// Now provide the implementation of the command with  registerCommand
	// The commandId parameter must match the command field in package.json
	let disposable = vscode.commands.registerCommand('codedescriber.GPTDescribe',generateFunctionDescription);
	context.subscriptions.push(disposable);
}

// This method is called when your extension is deactivated
function deactivate() {}

module.exports = {
	activate,
	deactivate
}

function generateFunctionDescription() {
    const editor = vscode.window.activeTextEditor;

    if (editor) {
		const selection = editor.selection;
        const selectedText = editor.document.getText(selection);

        const pythonProcess = spawn("python", [`${__dirname}/py_apps/GPTDescribe.py`, selectedText]);

        pythonProcess.stdout.on('data', (data) => {
            console.log(`stdout: ${data}`);
            // vscode.window.showInformationMessage('Description generated: ' + data);

			editor.edit(editBuilder => {
                editBuilder.insert(selection.start, data + "\n");
        });
		});

        pythonProcess.stderr.on('data', (data) => {
            console.error(`stderr: ${data}`);
            vscode.window.showErrorMessage(`Error generating description:  +  ${data}`);
        });

        pythonProcess.on('close', (code) => {
            console.log(`child process exited with code ${code}`);
        });

	}

}
