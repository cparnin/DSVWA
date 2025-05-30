#!/usr/bin/env python3
"""
Software Composition Analysis (SCA) scanner
Integrates with OSV and GitHub Advisory databases for dependency vulnerability scanning
"""

import json
import subprocess
import requests
import os
from pathlib import Path
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

def run_osv_scanner(repo_path: str) -> List[Dict[str, Any]]:
    """Run OSV scanner for dependency vulnerabilities"""
    try:
        # Install osv-scanner if not present
        result = subprocess.run(['osv-scanner', '--version'], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            logger.warning("OSV Scanner not found. Install with: go install github.com/google/osv-scanner/cmd/osv-scanner@v1")
            return []
            
        # Run OSV scanner
        output_file = Path("reports/osv-results.json")
        output_file.parent.mkdir(exist_ok=True)
        
        cmd = ['osv-scanner', '--format', 'json', '--output', str(output_file), repo_path]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if output_file.exists():
            with open(output_file) as f:
                data = json.load(f)
                return parse_osv_results(data)
        else:
            logger.error("OSV scanner failed to generate results")
            return []
            
    except Exception as e:
        logger.error(f"Error running OSV scanner: {e}")
        return []

def parse_osv_results(osv_data: Dict) -> List[Dict[str, Any]]:
    """Parse OSV scanner JSON output into normalized findings"""
    findings = []
    
    if 'results' not in osv_data:
        return findings
        
    for result in osv_data['results']:
        if 'packages' not in result:
            continue
            
        for package in result['packages']:
            if 'vulnerabilities' not in package:
                continue
                
            for vuln in package['vulnerabilities']:
                finding = {
                    'path': package.get('package', {}).get('source_file', 'requirements.txt'),
                    'line': 1,  # Could be enhanced to find actual line
                    'description': f"Vulnerable dependency: {package.get('package', {}).get('name', 'unknown')}",
                    'severity': map_osv_severity(vuln.get('severity', [])),
                    'vulnerability_id': vuln.get('id', 'unknown'),
                    'affected_package': package.get('package', {}).get('name'),
                    'affected_version': package.get('package', {}).get('version'),
                    'summary': vuln.get('summary', 'No summary available'),
                    'fixed_versions': extract_fixed_versions(vuln),
                    'tool': 'osv-scanner'
                }
                findings.append(finding)
    
    return findings

def map_osv_severity(severity_list: List[Dict]) -> str:
    """Map OSV severity to standard severity levels"""
    if not severity_list:
        return 'MEDIUM'
        
    # OSV uses CVSS scores
    for sev in severity_list:
        if sev.get('type') == 'CVSS_V3':
            score = float(sev.get('score', 0))
            if score >= 9.0:
                return 'CRITICAL'
            elif score >= 7.0:
                return 'HIGH'
            elif score >= 4.0:
                return 'MEDIUM'
            else:
                return 'LOW'
    
    return 'MEDIUM'

def extract_fixed_versions(vuln: Dict) -> List[str]:
    """Extract fixed versions from vulnerability data"""
    fixed_versions = []
    
    if 'affected' in vuln:
        for affected in vuln['affected']:
            if 'ranges' in affected:
                for range_info in affected['ranges']:
                    if 'events' in range_info:
                        for event in range_info['events']:
                            if 'fixed' in event:
                                fixed_versions.append(event['fixed'])
    
    return fixed_versions

def check_github_advisory(package_name: str, version: str) -> List[Dict[str, Any]]:
    """Check GitHub Advisory Database for specific package vulnerabilities"""
    try:
        # GitHub GraphQL API for security advisories
        query = """
        query($package: String!) {
          securityAdvisories(first: 10, orderBy: {field: PUBLISHED_AT, direction: DESC}) {
            nodes {
              ghsaId
              summary
              severity
              vulnerabilities(first: 10) {
                nodes {
                  package {
                    name
                  }
                  vulnerableVersionRange
                  firstPatchedVersion {
                    identifier
                  }
                }
              }
            }
          }
        }
        """
        
        # Note: This is a simplified implementation
        # In production, you'd want to use proper GitHub API authentication
        # and more sophisticated package matching
        
        return []  # Placeholder for now
        
    except Exception as e:
        logger.error(f"Error checking GitHub Advisory: {e}")
        return []

def generate_upgrade_suggestions(findings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Generate automated upgrade suggestions for vulnerable dependencies"""
    suggestions = []
    
    for finding in findings:
        if finding.get('tool') == 'osv-scanner' and finding.get('fixed_versions'):
            suggestion = {
                'package': finding.get('affected_package'),
                'current_version': finding.get('affected_version'),
                'recommended_version': finding.get('fixed_versions', [None])[-1],  # Latest fix
                'vulnerability_id': finding.get('vulnerability_id'),
                'severity': finding.get('severity'),
                'upgrade_command': f"pip install {finding.get('affected_package')}=={finding.get('fixed_versions', [None])[-1]}"
            }
            suggestions.append(suggestion)
    
    return suggestions

def run_sca_scan(repo_path: str) -> List[Dict[str, Any]]:
    """Main SCA scanning function"""
    logger.info("Running Software Composition Analysis...")
    
    findings = []
    
    # Run OSV scanner
    osv_findings = run_osv_scanner(repo_path)
    findings.extend(osv_findings)
    
    # Generate upgrade suggestions
    if findings:
        suggestions = generate_upgrade_suggestions(findings)
        logger.info(f"Generated {len(suggestions)} upgrade suggestions")
        
        # Save suggestions to file for potential auto-PR generation
        suggestions_file = Path("reports/upgrade-suggestions.json")
        with open(suggestions_file, 'w') as f:
            json.dump(suggestions, f, indent=2)
    
    return findings

if __name__ == "__main__":
    # Test the SCA scanner
    import sys
    repo_path = sys.argv[1] if len(sys.argv) > 1 else "."
    findings = run_sca_scan(repo_path)
    print(f"Found {len(findings)} dependency vulnerabilities")
    for finding in findings:
        print(f"  - {finding['affected_package']} {finding['affected_version']}: {finding['vulnerability_id']}")
