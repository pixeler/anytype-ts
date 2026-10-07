const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const rootDir = path.resolve(__dirname, '..');
const distDir = path.join(rootDir, 'dist');
const toolsDir = path.join(rootDir, 'tools');
const protocDir = path.join(toolsDir, 'protoc');
const protocBin = path.join(protocDir, 'bin');
const protocExe = path.join(protocBin, 'protoc.exe');

async function downloadFile(url, destPath) {
	console.log(`Downloading ${url}...`);
	execSync(`curl.exe -fSL -o "${destPath}" "${url}"`, { stdio: 'inherit' });
	console.log(`Downloaded to ${destPath}`);
}

async function main() {
	if (!fs.existsSync(toolsDir)) fs.mkdirSync(toolsDir, { recursive: true });
	if (!fs.existsSync(distDir)) fs.mkdirSync(distDir, { recursive: true });

	// 1. Setup protoc
	if (!fs.existsSync(protocExe)) {
		console.log('--- Setting up protoc ---');
		const protocZip = path.join(toolsDir, 'protoc.zip');
		await downloadFile('https://github.com/protocolbuffers/protobuf/releases/download/v23.4/protoc-23.4-win64.zip', protocZip);
		if (!fs.existsSync(protocDir)) fs.mkdirSync(protocDir, { recursive: true });
		console.log('Extracting protoc...');
		execSync(`tar.exe -xf "${protocZip}" -C "${protocDir}"`, { stdio: 'inherit' });
		if (fs.existsSync(protocZip)) fs.unlinkSync(protocZip);
		console.log('protoc installed successfully.');
	} else {
		console.log('protoc is already installed at:', protocExe);
	}

	// 2. Setup anytype-heart middleware
	const helperExe = path.join(distDir, 'anytypeHelper.exe');
	const protosDir = path.join(distDir, 'lib', 'protos');
	if (!fs.existsSync(helperExe) || !fs.existsSync(protosDir)) {
		console.log('--- Setting up anytype-heart middleware ---');
		const mwv = fs.readFileSync(path.join(rootDir, 'middleware.version'), 'utf8').trim();
		const zipName = `js_v${mwv}_windows-amd64.zip`;
		const zipUrl = `https://github.com/anyproto/anytype-heart/releases/download/v${mwv}/${zipName}`;
		const mwZip = path.join(rootDir, 'addon.zip');
		await downloadFile(zipUrl, mwZip);

		const extractDir = path.join(rootDir, 'mw_temp');
		if (fs.existsSync(extractDir)) fs.rmSync(extractDir, { recursive: true, force: true });
		fs.mkdirSync(extractDir, { recursive: true });

		console.log('Extracting middleware package...');
		execSync(`tar.exe -xf "${mwZip}" -C "${extractDir}"`, { stdio: 'inherit' });

		console.log('Organizing middleware files into dist/...');
		// copy grpc-server.exe -> dist/anytypeHelper.exe
		const grpcServer = path.join(extractDir, 'grpc-server.exe');
		if (fs.existsSync(grpcServer)) {
			fs.copyFileSync(grpcServer, helperExe);
		} else {
			console.warn('Could not find grpc-server.exe in extracted archive');
		}

		// Clean old protos & json
		const libDir = path.join(distDir, 'lib');
		['pb', 'pkg', 'protos'].forEach(dir => {
			const target = path.join(libDir, dir);
			if (fs.existsSync(target)) fs.rmSync(target, { recursive: true, force: true });
		});

		// Copy protobuf/* -> dist/lib/
		const protobufDir = path.join(extractDir, 'protobuf');
		if (fs.existsSync(protobufDir)) {
			fs.cpSync(protobufDir, libDir, { recursive: true });
		}

		// Copy json/* -> dist/lib/json/generated/
		const jsonSrc = path.join(extractDir, 'json');
		const jsonDst = path.join(libDir, 'json', 'generated');
		if (!fs.existsSync(jsonDst)) fs.mkdirSync(jsonDst, { recursive: true });
		if (fs.existsSync(jsonSrc)) {
			fs.cpSync(jsonSrc, jsonDst, { recursive: true });
		}

		// Cleanup temp
		fs.rmSync(extractDir, { recursive: true, force: true });
		if (fs.existsSync(mwZip)) fs.unlinkSync(mwZip);
		console.log('Middleware assets successfully placed into dist/');
	} else {
		console.log('anytypeHelper.exe and proto assets already present in dist/');
	}

	// 3. Generate TypeScript protobuf bindings and service registry
	console.log('--- Generating Protobuf TypeScript bindings ---');
	const bashExe = 'C:\\Program Files\\Git\\bin\\bash.exe';
	if (!fs.existsSync(bashExe)) {
		throw new Error('Git Bash not found at ' + bashExe);
	}

	// Set PATH to include protoc directory for bash
	const env = {
		...process.env,
		PATH: `${protocBin};${process.env.PATH}`,
	};

	execSync(`"${bashExe}" -c "bash scripts/generate-protos.sh --from-dist"`, {
		cwd: rootDir,
		env,
		stdio: 'inherit',
	});

	// 4. Update locale
	console.log('--- Updating locale ---');
	execSync('node ./electron/hook/locale.js', {
		cwd: rootDir,
		stdio: 'inherit',
	});

	console.log('\n=== Windows Setup Complete! ===');
	console.log('You can now run:');
	console.log('  bun run start:dev-win    (to test running in dev mode)');
	console.log('  bun run dist:win         (to package the Windows installer)');
}

main().catch(err => {
	console.error('Setup failed:', err);
	process.exit(1);
});
